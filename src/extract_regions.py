''' 
#Uso
python extract_regions.py --gff genes.gff --fasta genome.fasta --up 500 --down 50 --out regions.fna

#Objetivo
Para cada gene en el archivo GFF:
1. Obtener región upstream de tamaño --up.
2. Obtener región downstream de tamaño --down.
3. Considerar correctamente el strand:
    - strand +: upstream = antes; downstream = después.
    - strand -: upstream = después; downstream = antes.
4. Incluir coordenadas genómicas reales en los encabezados FASTA.

#Formato esperado del encabezado FASTA
Cada secuencia debe incluir:
- el ID del gene
- si es upstream o downstream
- coordenadas genómicas exactas (start-end)
- strand del gen
- coordenadas originales del gene

Ejemplo de salida para strand +:
>araC_upstream 12345-12844 strand=+ original_gene_coords=12845-13500
ATGCTAGCTAGCTAGGCTAGCTACGTAC
>araC_downstream 13501-13550 strand=+ original_gene_coords=12845-13500
TTTTTTGCGCGATTAACCCTT

Ejemplo de salida para strand -:
>geneX_upstream 8801-9300 strand=- original_gene_coords=8000-8799
ACGTGCGTACGTACGTAGCG
>geneX_downstream 7500-7999 strand=- original_gene_coords=8000-8799
TTAAGCCGTTTTTTGCGGTA
'''

import argparse
#TODO: importar otras librerías si es necesario

def parse_arguments():
    '''
    TODO: Implementar el parseo de argumentos
    --gff: ruta al archivo GFF. Obligatorio. Debe terminar en .gff o .gff3
    --fasta: ruta al archivo FASTA. Obligatorio. Debe terminar en .fasta o .fa
    --up: tamaño de región upstream. Opcional, default 1000.
    --down: tamaño de región downstream. Opcional, default 1000.
    --out: ruta al archivo de salida FASTA. Obligatorio. Debe terminar en .fna o .fasta
    '''
    pass


def load_fasta(fasta_path: str) -> dict:
    '''
    TODO: Implementar la carga del archivo FASTA
    - Input: ruta al archivo FASTA
    - Output: diccionario {seq_id: sequence}
    '''
    pass

def parse_gff(gff_path: str) -> list:
    '''
    TODO: Implementar el parseo del archivo GFF
    - Input: ruta al archivo GFF
    - Output: lista de diccionarios con info de cada gene:
        [
            {
                'seqid': 'chr1',
                'source': 'source',
                'type': 'gene',
                'start': 100,
                'end': 500,
                'score': '.',
                'strand': '+',
                'phase': '.',
                'attributes': {'ID': 'gene1', 'Name': 'gene_name1'}
            },
            ...
        ]
    '''  
    pass

def upstream_downstream_coords(gene_record: dict, up: int, down: int) -> tuple:
    '''
    TODO: Implementar el cálculo de coordenadas upstream y downstream
    - Input:
        - gene_record: diccionario con info de un gene
        - up: tamaño de región upstream
        - down: tamaño de región downstream
    - Output: tupla con coordenadas (up_start, up_end, down_start, down_end)
    Considerar el strand para definir upstream y downstream
    '''
    pass

def join_header_and_sequence(header: str, sequence: str) -> str:
    '''
    TODO: Implementar la creación del encabezado FASTA
    - Input:
        - header: string con el encabezado FASTA
        - sequence: string con la secuencia
    - Output: string con el formato FASTA completo y acomodado en parts de 60 caracteres por línea
    '''

def extract_region(seqs_from_FASTA: dict, gene_record_from_GFF: dict, up: int, down: int) -> list:
    '''
    TODO: Implementar la extracción de regiones upstream y downstream
    - Input:
        - seqs_from_FASTA: diccionario {seq_id: sequence}
        - gene_record_from_GFF: diccionario con info de un o los gene(s)
        - up: tamaño de región upstream
        - down: tamaño de región downstream
    - Output: lista de tuplas (header, sequence) para upstream y downstream
    Debe considerar el strand para definir upstream y downstream
    '''
    pass

def main():
    #TODO: implementar la lógica principal del script
    pass

if __name__ == "__main__":
    main()
