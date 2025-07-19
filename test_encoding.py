#!/usr/bin/env python3
"""
Script para probar el manejo de codificaciones en el archivo repository
"""

from src.infrastructure.repositories.file_repository import FileRepository
import sys

def main():
    print("🔧 Probando el nuevo sistema de codificación...")
    
    repo = FileRepository()
    archivos = repo.listar_archivos_expedientes()
    
    print(f"📁 Archivos encontrados: {len(archivos)}")
    
    if not archivos:
        print("❌ No hay archivos de expedientes para probar")
        return
    
    # Probar con los primeros 3 archivos
    archivos_a_probar = archivos[:3]
    
    exitosos = 0
    errores = 0
    
    for archivo in archivos_a_probar:
        archivo_sin_ext = archivo.replace('.edf', '')
        print(f"\n📄 Probando archivo: {archivo}")
        
        try:
            # Probar lectura de información
            carne, nombre = repo.leer_informacion_estudiante(archivo_sin_ext)
            print(f"✅ Info leída: {carne} - {nombre}")
            
            # Probar lectura de historial
            historial = repo.leer_historial(archivo_sin_ext)
            print(f"✅ Historial leído: {len(historial)} registros")
            
            exitosos += 1
            
        except FileNotFoundError as e:
            print(f"❌ Archivo no encontrado: {e}")
            errores += 1
        except UnicodeDecodeError as e:
            print(f"❌ Error de codificación: {e}")
            errores += 1
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            errores += 1
    
    print(f"\n📊 Resultados:")
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Errores: {errores}")
    
    if errores == 0:
        print("🎉 ¡Todos los archivos se leyeron correctamente!")
        print("🔧 El problema de codificación ha sido resuelto.")
    else:
        print("⚠️  Algunos archivos aún tienen problemas.")

if __name__ == "__main__":
    main()
