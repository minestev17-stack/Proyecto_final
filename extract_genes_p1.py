'''
Uso
python extract_genes.py --gff genes.gff --fasta genome.fasta --output genes.fna

Objetivo
- Leer un archivo FASTA con el genoma completo.
- Leer un archivo GFF.
- Extraer las secuencias DNA correspondientes a las features gene.
- Guardarlas en un archivo FASTA de salida.

Ejemplo de salida esperada (genes.fna)
>araC  gene_coords=3456-41020 strand=+
ATGCGTAGCTAGCTAGCTAGCTAA
>crp  gene_coords=3456-41020 strand=-
ATTTGCGCGGCGCGCGTTAG

Requisitos Tecnicos
argparse obligatorio.
Funciones: load_fasta(), parse_gff(), extract_gene_seqs().
Manejo de errores con excepciones.
Docstrings y PEP8.
Pruebas con asserts + documento de pruebas, bien con pytest.
'''

# TODO: Implementar el script extract_genes.py segun las especificaciones dadas.

import argparse
# TODO: Importar otros modulos necesarios


def load_fasta():
    '''
    TODO: Implementar la funcion para cargar un archivo FASTA.
    Debe devolver un diccionario con los IDs de secuencia como claves
    y las secuencias como valores, tambien incluir el nombre del gen (solo si tiene) y su longitud.
    Returns:
        dict: Diccionario con las secuencias del archivo FASTA.
    '''

    return

def parse_gff():
    '''
     TODO: Implementar el paso de argumentos con el modulo argparse.
     - --gff: ruta al archivo GFF de entrada. Solo puede admitir archivos .gff
     - --fasta: ruta al archivo FASTA de entrada. Solo puede admitir archivos .fasta
     - --output: ruta al archivo FASTA de salida. Solo puede admitir archivos .fna
     - Todos los argumentos son obligatorios.
     - Incluir mensajes de ayuda para cada argumento.
        Returns:
            argparse.Namespace: Objeto con los argumentos parseados.
 '''

    return

def extract_gene_seqs():