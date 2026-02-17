#!/usr/bin/env python3
"""
consolidate_part2_to_csv.py

Consolida todas las hojas de Práctica II de todos los estudiantes
en un único archivo CSV.
"""

import openpyxl
import xlrd
import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('consolidation.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def is_part2_sheet(sheet, sheet_name: str) -> bool:
    """
    Detecta si una hoja contiene datos Part II.
    
    Criterios:
    1. NO debe ser una hoja "Values" (son resúmenes)
    2. Debe contener al menos 2 de 3 indicadores:
       - "Elements to be identified"
       - "Value" como header
       - "E2R Guideline" o "E2R Analysis"
    """
    # Excluir hojas de resumen
    if 'value' in sheet_name.lower() and sheet_name.lower().startswith('value'):
        return False
    
    found_elements = False
    found_value = False
    found_e2r = False
    
    try:
        # Manejar tanto openpyxl como xlrd
        if hasattr(sheet, 'iter_rows'):  # openpyxl
            # Para openpyxl, obtener max_row de forma segura
            try:
                max_row = min(20, sheet.max_row or 20)
            except:
                max_row = 20
            
            for i in range(1, max_row + 1):
                row = list(sheet.iter_rows(min_row=i, max_row=i, values_only=True))
                if row and row[0]:
                    row_text = ' '.join([str(cell).lower() if cell else '' for cell in row[0]])
                    
                    if 'elements to be identified' in row_text:
                        found_elements = True
                    if 'value' in row_text and i < 15:
                        found_value = True
                    if 'e2r guideline' in row_text or 'e2r analysis' in row_text:
                        found_e2r = True
        else:  # xlrd
            max_row = min(20, sheet.nrows)
            for i in range(max_row):
                try:
                    row = sheet.row_values(i)
                    row_text = ' '.join([str(cell).lower() if cell else '' for cell in row])
                    
                    if 'elements to be identified' in row_text:
                        found_elements = True
                    if 'value' in row_text and i < 15:
                        found_value = True
                    if 'e2r guideline' in row_text or 'e2r analysis' in row_text:
                        found_e2r = True
                except:
                    continue
    except Exception as e:
        logger.debug(f"Error checking sheet {sheet_name}: {e}")
        return False
    
    score = sum([found_elements, found_value, found_e2r])
    return score >= 2


def extract_metadata_openpyxl(sheet) -> Dict[str, str]:
    """Extrae metadatos de las primeras filas (openpyxl)."""
    metadata = {
        'web': '',
        'evaluators': '',
        'tool': '',
        'comment': '',
        'time': ''
    }
    
    # Buscar en primeras 10 filas
    for row in sheet.iter_rows(max_row=10, values_only=True):
        if not row or not row[0]:
            continue
        
        key = str(row[0]).strip().lower()
        value = str(row[1]).strip() if len(row) > 1 and row[1] else ''
        
        if 'web site' in key:
            metadata['web'] = value
        elif 'evaluator' in key:
            metadata['evaluators'] = value
        elif 'tool used' in key:
            metadata['tool'] = value
        elif 'comment' in key:
            metadata['comment'] = value
        elif 'time spent' in key:
            metadata['time'] = value
    
    return metadata


def extract_metadata_xlrd(sheet) -> Dict[str, str]:
    """Extrae metadatos de las primeras filas (xlrd)."""
    metadata = {
        'web': '',
        'evaluators': '',
        'tool': '',
        'comment': '',
        'time': ''
    }
    
    # Buscar en primeras 10 filas
    for i in range(min(10, sheet.nrows)):
        try:
            row = sheet.row_values(i)
            if not row or not row[0]:
                continue
            
            key = str(row[0]).strip().lower()
            value = str(row[1]).strip() if len(row) > 1 and row[1] else ''
            
            if 'web site' in key:
                metadata['web'] = value
            elif 'evaluator' in key:
                metadata['evaluators'] = value
            elif 'tool used' in key:
                metadata['tool'] = value
            elif 'comment' in key:
                metadata['comment'] = value
            elif 'time spent' in key:
                metadata['time'] = value
        except:
            continue
    
    return metadata


def find_data_start_row_openpyxl(sheet) -> Optional[int]:
    """Encuentra la fila donde comienzan los datos (openpyxl)."""
    for i, row in enumerate(sheet.iter_rows(values_only=True), 1):
        row_text = ' '.join([str(cell).lower() if cell else '' for cell in row])
        if 'elements to be identified' in row_text and 'value' in row_text:
            return i
    return None


def find_data_start_row_xlrd(sheet) -> Optional[int]:
    """Encuentra la fila donde comienzan los datos (xlrd)."""
    for i in range(sheet.nrows):
        try:
            row = sheet.row_values(i)
            row_text = ' '.join([str(cell).lower() if cell else '' for cell in row])
            if 'elements to be identified' in row_text and 'value' in row_text:
                return i
        except:
            continue
    return None


def extract_data_rows_openpyxl(sheet, start_row: int) -> List[Dict[str, str]]:
    """Extrae filas de datos desde start_row (openpyxl)."""
    data_rows = []
    current_category = 'E2R Guidelines about Spelling'  # Default inicial
    
    for row in sheet.iter_rows(min_row=start_row + 1, values_only=True):
        # Verificar si es fila vacía (fin de datos)
        if not any(cell for cell in row if cell):
            break
        
        # Columnas: A(vacía), B(Element), C(Value), D(Details), E(Comments)
        col_b = str(row[1]).strip() if len(row) > 1 and row[1] else ''
        col_c = str(row[2]).strip() if len(row) > 2 and row[2] else ''
        col_d = str(row[3]).strip() if len(row) > 3 and row[3] else ''
        col_e = str(row[4]).strip() if len(row) > 4 and row[4] else ''
        
        # Si es una categoría E2R, actualizar current_category
        if 'e2r guideline' in col_b.lower():
            current_category = col_b
            continue
        
        # Si no hay elemento, saltar
        if not col_b:
            continue
        
        # Si encontramos "Value" + "Meaning" significa que es una hoja Values
        if 'value' in col_b.lower() and 'meaning' in col_c.lower():
            break
        
        data_rows.append({
            'category': current_category,
            'element': col_b,
            'value': col_c,
            'details': col_d,
            'comments': col_e
        })
    
    return data_rows


def extract_data_rows_xlrd(sheet, start_row: int) -> List[Dict[str, str]]:
    """Extrae filas de datos desde start_row (xlrd)."""
    data_rows = []
    current_category = 'E2R Guidelines about Spelling'  # Default inicial
    
    for i in range(start_row + 1, sheet.nrows):
        try:
            row = sheet.row_values(i)
            
            # Verificar si es fila vacía
            if not any(cell for cell in row if cell):
                break
            
            col_b = str(row[1]).strip() if len(row) > 1 and row[1] else ''
            col_c = str(row[2]).strip() if len(row) > 2 and row[2] else ''
            col_d = str(row[3]).strip() if len(row) > 3 and row[3] else ''
            col_e = str(row[4]).strip() if len(row) > 4 and row[4] else ''
            
            # Si es categoría E2R
            if 'e2r guideline' in col_b.lower():
                current_category = col_b
                continue
            
            if not col_b:
                continue
            
            if 'value' in col_b.lower() and 'meaning' in col_c.lower():
                break
            
            data_rows.append({
                'category': current_category,
                'element': col_b,
                'value': col_c,
                'details': col_d,
                'comments': col_e
            })
        except:
            continue
    
    return data_rows


def process_sheet_openpyxl(sheet, sheet_name: str, file_path: Path, group_num: int) -> List[Dict[str, str]]:
    """Procesa una hoja completa (openpyxl)."""
    logger.info(f"  Processing sheet: {sheet_name}")
    
    # Extraer metadatos
    metadata = extract_metadata_openpyxl(sheet)
    
    # Encontrar inicio de datos
    start_row = find_data_start_row_openpyxl(sheet)
    if not start_row:
        logger.warning(f"    No data header found in {sheet_name}")
        return []
    
    # Extraer datos
    data_rows = extract_data_rows_openpyxl(sheet, start_row)
    
    # Combinar con metadatos
    result = []
    for data in data_rows:
        result.append({
            'E2R Guidelines': data['category'],
            'Elements to be identified': data['element'],
            'Value': data['value'],
            'Details': data['details'],
            'Comments': data['comments'],
            'Tool used': metadata['tool'],
            'Comment': metadata['comment'],
            'Time Spent': metadata['time'],
            'Group': str(group_num),
            'Web': metadata['web']
        })
    
    logger.info(f"    Extracted {len(result)} rows")
    return result


def process_sheet_xlrd(sheet, sheet_name: str, file_path: Path, group_num: int) -> List[Dict[str, str]]:
    """Procesa una hoja completa (xlrd)."""
    logger.info(f"  Processing sheet: {sheet_name}")
    
    metadata = extract_metadata_xlrd(sheet)
    start_row = find_data_start_row_xlrd(sheet)
    
    if not start_row:
        logger.warning(f"    No data header found in {sheet_name}")
        return []
    
    data_rows = extract_data_rows_xlrd(sheet, start_row)
    
    result = []
    for data in data_rows:
        result.append({
            'E2R Guidelines': data['category'],
            'Elements to be identified': data['element'],
            'Value': data['value'],
            'Details': data['details'],
            'Comments': data['comments'],
            'Tool used': metadata['tool'],
            'Comment': metadata['comment'],
            'Time Spent': metadata['time'],
            'Group': str(group_num),
            'Web': metadata['web']
        })
    
    logger.info(f"    Extracted {len(result)} rows")
    return result


def process_excel_file(file_path: Path, group_num: int) -> List[Dict[str, str]]:
    """Procesa todas las hojas de un archivo Excel."""
    all_rows = []
    
    try:
        # Primero intentar con openpyxl (funciona para .xlsx y algunos .xls mal nombrados)
        try:
            wb = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
            
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                
                if is_part2_sheet(sheet, sheet_name):
                    rows = process_sheet_openpyxl(sheet, sheet_name, file_path, group_num)
                    all_rows.extend(rows)
            
            wb.close()
            return all_rows
        
        except Exception as e1:
            # Si falla openpyxl, intentar con xlrd (para .xls antiguos reales)
            if file_path.suffix.lower() == '.xls':
                try:
                    wb = xlrd.open_workbook(str(file_path))
                    
                    for sheet_name in wb.sheet_names():
                        sheet = wb.sheet_by_name(sheet_name)
                        
                        if is_part2_sheet(sheet, sheet_name):
                            rows = process_sheet_xlrd(sheet, sheet_name, file_path, group_num)
                            all_rows.extend(rows)
                    
                    return all_rows
                except Exception as e2:
                    # Special case: xlrd says "Excel xlsx file; not supported"
                    # This means it's actually xlsx format with wrong .XLS extension
                    if "xlsx file; not supported" in str(e2).lower():
                        logger.info(f"  Detected xlsx format with .XLS extension, renaming temporarily...")
                        import shutil
                        temp_path = file_path.with_suffix('.xlsx')
                        shutil.copy2(file_path, temp_path)
                        try:
                            wb = openpyxl.load_workbook(temp_path, data_only=True, read_only=True)
                            
                            for sheet_name in wb.sheetnames:
                                sheet = wb[sheet_name]
                                
                                if is_part2_sheet(sheet, sheet_name):
                                    rows = process_sheet_openpyxl(sheet, sheet_name, file_path, group_num)
                                    all_rows.extend(rows)
                            
                            wb.close()
                            return all_rows
                        finally:
                            # Clean up temp file
                            if temp_path.exists():
                                temp_path.unlink()
                    else:
                        logger.error(f"  Error processing {file_path.name}: {e2}")
            else:
                logger.error(f"  Error processing {file_path.name}: {e1}")
    
    except Exception as e:
        logger.error(f"  Error processing {file_path.name}: {e}")
    
    return all_rows


def find_all_part2_data() -> Tuple[List[Dict[str, str]], Dict[str, int], List[str]]:
    """
    Busca todos los archivos y hojas con datos Part II.
    
    Returns:
        (all_rows, group_mapping, groups_without_data)
    """
    base_dir = Path('/home/javi/practices')
    student_dirs = sorted([d for d in base_dir.glob('*_assignsubmission_file')])
    
    # Crear mapeo de grupos
    group_mapping = {d.name: idx + 1 for idx, d in enumerate(student_dirs)}
    
    all_rows = []
    groups_without_data = []
    
    logger.info(f"Found {len(student_dirs)} student directories")
    logger.info("=" * 80)
    
    for student_dir in student_dirs:
        student_name = student_dir.name.split('_')[0]
        group_num = group_mapping[student_dir.name]
        
        logger.info(f"\nGroup {group_num}: {student_name}")
        
        # Buscar todos los archivos Excel (case-insensitive)
        xlsx_files = list(student_dir.glob('*.xlsx')) + list(student_dir.glob('*.XLSX'))
        xls_files = list(student_dir.glob('*.xls')) + list(student_dir.glob('*.XLS'))
        all_excel_files = xlsx_files + xls_files
        
        if not all_excel_files:
            logger.warning(f"  No Excel files found")
            groups_without_data.append(f"{group_num}. {student_name}")
            continue
        
        student_rows = []
        for excel_file in all_excel_files:
            logger.info(f"  File: {excel_file.name}")
            rows = process_excel_file(excel_file, group_num)
            student_rows.extend(rows)
        
        if student_rows:
            all_rows.extend(student_rows)
            logger.info(f"  ✓ Total rows for this group: {len(student_rows)}")
        else:
            logger.warning(f"  ✗ No Part II data found")
            groups_without_data.append(f"{group_num}. {student_name}")
    
    return all_rows, group_mapping, groups_without_data


def write_csv(all_rows: List[Dict[str, str]], output_path: Path):
    """Escribe el CSV consolidado."""
    if not all_rows:
        logger.error("No data to write!")
        return
    
    headers = [
        'E2R Guidelines',
        'Elements to be identified',
        'Value',
        'Details',
        'Comments',
        'Tool used',
        'Comment',
        'Time Spent',
        'Group',
        'Web'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(all_rows)
    
    logger.info(f"\n✅ CSV written to: {output_path}")
    logger.info(f"   Total rows: {len(all_rows)}")


def write_report(all_rows: List[Dict[str, str]], group_mapping: Dict[str, int], 
                 groups_without_data: List[str], report_path: Path):
    """Genera reporte de consolidación."""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE CONSOLIDACIÓN - PRÁCTICA II\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("ESTADÍSTICAS:\n")
        f.write(f"  • Total de grupos: {len(group_mapping)}\n")
        f.write(f"  • Grupos con datos: {len(group_mapping) - len(groups_without_data)}\n")
        f.write(f"  • Grupos sin datos: {len(groups_without_data)}\n")
        f.write(f"  • Total de filas CSV: {len(all_rows)}\n\n")
        
        if groups_without_data:
            f.write("⚠️  GRUPOS SIN PRÁCTICA II:\n")
            for group in groups_without_data:
                f.write(f"  {group}\n")
            f.write("\n")
        
        # Distribución por grupo
        f.write("\nDISTRIBUCIÓN DE FILAS POR GRUPO:\n")
        group_counts = {}
        for row in all_rows:
            group = row['Group']
            group_counts[group] = group_counts.get(group, 0) + 1
        
        for group_num in sorted(group_counts.keys(), key=int):
            count = group_counts[group_num]
            f.write(f"  Grupo {group_num}: {count} filas\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    logger.info(f"📄 Report written to: {report_path}")


def main():
    """Función principal."""
    logger.info("Starting Part II consolidation...")
    logger.info("=" * 80)
    
    # Buscar todos los datos
    all_rows, group_mapping, groups_without_data = find_all_part2_data()
    
    logger.info("\n" + "=" * 80)
    logger.info("CONSOLIDATION COMPLETE")
    logger.info("=" * 80)
    
    if not all_rows:
        logger.error("❌ No data found to consolidate!")
        return
    
    # Escribir CSV
    csv_path = Path('/home/javi/practices/part2_consolidated.csv')
    write_csv(all_rows, csv_path)
    
    # Escribir reporte
    report_path = Path('/home/javi/practices/consolidation_report.txt')
    write_report(all_rows, group_mapping, groups_without_data, report_path)
    
    logger.info("\n✅ All done!")
    logger.info(f"   CSV: {csv_path}")
    logger.info(f"   Report: {report_path}")
    logger.info(f"   Log: consolidation.log")


if __name__ == '__main__':
    main()
