#!/usr/bin/env python3
"""
extract_genes.py

Herramienta CLI para extraer secuencias de genes de un genoma FASTA utilizando coordenadas de un archivo GFF.

Uso:
    python extract_genes.py --gff genes.gff --fasta genome.fasta --output genes.fna

Autor: PyLIA (generated)
Revisor: Leonardo Daniel González López
1 de diciembre de 2025
"""

from __future__ import annotations

import argparse
import os
from typing import Dict, List, Tuple


def parse_args() -> argparse.Namespace:
    """
    Parsea y valida los argumentos de la línea de comandos.

    Returns:
        argparse.Namespace: Argumentos parseados con atributos gff, fasta, output.
    """
    parser = argparse.ArgumentParser(
        description="Extrae secuencias de genes de un genoma FASTA usando un archivo GFF."
    )

    def _file_must_exist_and_ext(path: str, exts: Tuple[str, ...]) -> str:
        if not os.path.exists(path): #Si el archivo no existe
            raise argparse.ArgumentTypeError(f"File not found: {path}")
        if not any(path.lower().endswith(ext) for ext in exts): #Si la extension no es correcta
            raise argparse.ArgumentTypeError(
                f"File '{path}' must have one of extensions: {', '.join(exts)}"
            )
        return path

    parser.add_argument(
        "--gff",
        required=True,
        type=lambda p: _file_must_exist_and_ext(p, (".gff", ".gff3")), #Valida que el archivo exista donde p es la ruta que se pasa solo si existe y tiene la extension correcta con la lista de extensiones
        help="Camino al archivo GFF de entrada (requerido). Extensiones aceptadas: .gff, .gff3",
    )
    parser.add_argument(
        "--fasta",
        required=True,
        type=lambda p: _file_must_exist_and_ext(p, (".fasta", ".fa")),
        help="Camino al genoma FASTA de entrada (requerido). Extensiones aceptadas: .fasta, .fa",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=lambda p: p if p.lower().endswith(".fna") else argparse.ArgumentTypeError( #Si lo ingresado termina en .fna lo devuelve, si no lanza un error
            "El output debe terminar en .fna"
        ),
        help="Camino al archivo FASTA de salida (requerido). Debe terminar en .fna",
    )

    args = parser.parse_args()
    #Si el tipo devuelto es un objeto de excepción, argparse no lanzará; verificar:
    if isinstance(args.output, Exception):
        raise argparse.ArgumentTypeError(str(args.output))
    return args


def load_fasta(fasta_path: str) -> Dict[str, str]:
    """
    Carga un archivo FASTA en un diccionario que mapea seqid -> secuencia (mayúsculas, sin nuevas líneas).

    El seqid es tomado como la primera palabra después de '>' (dividiendo por espacios en blanco).

    Args:
        fasta_path (str): Camino al archivo FASTA.

    Returns:
        Dict[str, str]: Mapeo de seqid a secuencia.

    Da:
        FileNotFoundError: Si fasta_path no existe.
        ValueError: Si el formato FASTA es invalido.
    """
    if not os.path.exists(fasta_path):
        raise FileNotFoundError(f"FASTA file not found: {fasta_path}")

    fasta_dict: Dict[str, str] = {} #Diccionario para guardar las secuencias. En la llave va el identificador y en el valor la secuencia.
    current_id = None #Identificador de secuencia actual
    seq_parts: List[str] = [] #Partes de la secuencia actual

    with open(fasta_path, "r", encoding="utf-8") as fh: #Abre el archivo fasta en modo lectura
        for lineno, line in enumerate(fh, start=1): #Itera sobre cada linea del archivo
            line = line.rstrip("\n") #Elimina el salto de linea al final
            if not line: #Si la linea esta vacia,
                continue #pasa a la siguiente iteracion
            if line.startswith(">"): #Si la linea empieza con '>' (indica un encabezado de secuencia)
                if current_id is not None: #Si ya hay un identificador actual (ya se leyo una secuencia)
                    fasta_dict[current_id] = "".join(seq_parts).upper() #Guarda la secuencia en el diccionario, uniendola y convirtiendola a mayusculas
                header = line[1:].strip() #Elimina el '>' y espacios en blanco alrededor del encabezado
                if not header: #Si el encabezado esta vacio (tras el '>')
                    raise ValueError(f"Empty FASTA header at line {lineno}") #Lanza un error
                # seqid: Primer token antes del primer espacio en blanco del encabezado 
                current_id = header.split()[0] #Toma el primer token del encabezado como identificador de secuencia 
                seq_parts = [] #Lista vacia para las partes de la secuencia nueva
            else: #Si la linea no empieza con '>' (es parte de la secuencia)
                if current_id is None: #Si no hay un identificador actual (no se ha leido un encabezado antes)
                    raise ValueError( 
                        f"Found sequence data before header in FASTA at line {lineno}" 
                    )
                seq_parts.append(line.strip()) #Agrega la linea (sin espacios en blanco alrededor) a las partes de la secuencia

        if current_id is not None: #Despues de terminar de leer el archivo, si hay un identificador actual
            fasta_dict[current_id] = "".join(seq_parts).upper() #Guarda la ultima secuencia en el diccionario

    if not fasta_dict: #Si el diccionario esta vacio (no se encontro ninguna secuencia)
        raise ValueError(f"No sequences found in FASTA file: {fasta_path}") #Lanza un error

    return fasta_dict #Devuelve el diccionario con las secuencias


def _parse_attributes(attr_str: str) -> Dict[str, str]:
    """
    Parsea la columna de atributos del GFF (pares clave=valor separados por ';').

    Argumentos:
        attr_str (str): Atributos tipo string del GFF.

    Returns:
        Dict[str, str]: Mapeo de atributos clave-valor.
    """
    attrs: Dict[str, str] = {} #Diccionario para guardar los atributos
    for part in attr_str.strip().split(";"): #Divide la cadena de atributos por ';' e itera sobre cada parte
        if not part: #Si la parte esta vacia
            continue 
        if "=" in part: #Si la parte contiene '=' (formato clave=valor) 
            key, val = part.split("=", 1) #Divide por el primer '=' en clave y valor
            attrs[key] = val.strip() #Guarda en el diccionario, eliminando espacios en blanco alrededor del valor
        elif " " in part:
            #Algunos GFFs usan clave valor con espacios (menos común); intenta dividir por el primer espacio
            key, val = part.split(" ", 1) #Se hace lo mismo que en el if de arriba
            attrs[key] = val.strip()
        else:
            #fallback: guardar como flag
            attrs[part] = ""
    return attrs #Devuelve el diccionario de atributos


def parse_gff(gff_path: str) -> List[Dict]:
    """
    Parsea un archivo GFF/GFF3 y devuelve una lista de registros de genes.

    Solo características con tipo 'gene' (insensible a mayúsculas) son devueltas.

    Cada registro es un dict con claves: seqid, source, type, start, end, score, strand, phase, attributes (dict).

    Argumentos:
        gff_path (str): Path al archivo GFF.

    Returns:
        List[Dict]: Lista de registros de genes.

    Raises:
        FileNotFoundError: Si gff_path no existe.
        ValueError: Si el formato GFF es inválido.
    """
    if not os.path.exists(gff_path): #Si el archivo no existe
        raise FileNotFoundError(f"GFF file not found: {gff_path}")

    genes: List[Dict] = [] #La lista para guardar los registros de genes
    with open(gff_path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1): #Itera sobre cada linea del archivo
            line = line.strip() 
            if not line or line.startswith("#"): #Si la linea esta vacia o es un comentario
                continue
            cols = line.split("\t") #Divide la linea por tabulaciones en columnas
            if len(cols) < 9: #Si hay menos de 9 columnas (formato GFF invalido)
                raise ValueError(f"Malformed GFF at line {lineno}: expected >=9 columns")
            seqid, source, feature_type, start, end, score, strand, phase, attrs = cols[:9] #Asigna las primeras 9 columnas a variables
            if feature_type.lower() != "gene": #Si el tipo de caracteristica no es 'gene' (insensible a mayusculas)
                continue
            try: #Intenta convertir start y end a enteros
                start_i = int(start)
                end_i = int(end)
            except ValueError:
                raise ValueError(f"Invalid coordinates at line {lineno}: {start}-{end}")

            attributes = _parse_attributes(attrs) #Parsea la columna de atributos (ultima columna y puede tener varia información) usando la funcion definida arriba
            genes.append(
                {
                    "seqid": seqid,
                    "source": source,
                    "type": feature_type,
                    "start": start_i,
                    "end": end_i,
                    "score": score,
                    "strand": strand,
                    "phase": phase,
                    "attributes": attributes,
                    "line_no": lineno,
                }
            ) #Agrega el registro del gen a la lista de genes, cada palabra entre "" es el nombre de la clave y lo que esta despues de : es el valor asociado a esa clave
    return genes


def _reverse_complement(seq: str) -> str:
    """
    Devuelve el complemento inverso de una secuencia de ADN.

    Argumentos:
        seq (str): Secuencia de DNA.

    Returns:
        str: Secuencia en inverso complemento.
    """
    comp_map = str.maketrans("ACGTacgtNn", "TGCAtgcaNn") #Mapa de traduccion para complementar bases
    return seq.translate(comp_map)[::-1] #Traduce la secuencia usando el mapa y luego la invierte 


def _wrap_seq(seq: str, width: int = 60) -> str:
    """
    Envuuelve la secuencia en líneas de ancho dado.

    Argumentos:
        seq (str): La secuencia en string.
        width (int): Ancho de la linea.

    Returns:
        str: Secuencia envuelta con nueva línea al final.
    """
    return "\n".join(seq[i : i + width] for i in range(0, len(seq), width)) #Genera lineas de ancho dado y las une con saltos de linea, para que no sea una sola linea larga


def extract_gene_seqs(fasta_dict: Dict[str, str], gff_records: List[Dict], output_file: str) -> None:
    """
    Extrae secuencias de genes de fasta_dict según gff_records y escribe en output_file.

    Header format:
        >{name}  gene_coords={start}-{end} strand={strand}

    Name resolution precedence: attributes['Name'] > attributes['ID'] > gene_{index}

    Argumentos:
        fasta_dict (Dict[str, str]): Mapping seqid -> sequence.
        gff_records (List[Dict]): Lista de registros de genes GFF (parseados).
        output_file (str): Path de salida FASTA.

    Raises:
        ValueError: Si el seqid no se encuentra en fasta_dict o si las coordenadas son inválidas.
        OSError: Si el output_file no puede ser escrito.
    """
    if not gff_records:
        raise ValueError("No gene records provided (gff_records is empty).")

    with open(output_file, "w", encoding="utf-8") as outfh:
        gene_counter = 0
        for rec in gff_records: #Itera sobre cada registro de gen en la lista
            gene_counter += 1
            seqid = rec["seqid"] #Identificador de secuencia
            start = rec["start"] #Coordenada de inicio
            end = rec["end"] #Coordenada de fin
            strand = rec["strand"] #Hebra (+ o -)
            attrs = rec.get("attributes", {}) #Atributos del gen

            # Determina el nombre del gen con la precedencia dada
            name = attrs.get("Name") or attrs.get("ID") or f"gene_{gene_counter}"

            if seqid not in fasta_dict: #Si el identificador de secuencia no esta en el diccionario de secuencias
                raise ValueError(f"Sequence ID '{seqid}' (GFF line {rec.get('line_no')}) not found in FASTA.")

            contig_seq = fasta_dict[seqid] #Obtiene la secuencia del contig correspondiente al seqid
            contig_len = len(contig_seq) #Longitud de la secuencia del contig

            if start < 1 or end < 1 or start > end:
                raise ValueError(
                    f"Invalid coordinates for gene {name} on {seqid}: start={start}, end={end}"
                )
            if end > contig_len:
                raise ValueError(
                    f"Coordinates out of range for gene {name} on {seqid}: end={end} > contig_length={contig_len}"
                )

            # GFF is 1-based inclusive
            subseq = contig_seq[start - 1 : end] #Extrae la subsecuencia del contig usando las coordenadas del gen

            if strand == "-": #Si la hebra es negativa
                subseq = _reverse_complement(subseq)

            header = f">{name}  gene_coords={start}-{end} strand={strand}" #Crea el encabezado del gen con la informacion requerida
            outfh.write(header + "\n") #Escribe el encabezado en el archivo de salida
            outfh.write(_wrap_seq(subseq) + "\n") #Escribe la secuencia envuelta en el archivo de salida


def main() -> None:
    args = parse_args()
    fasta_dict = load_fasta(args.fasta)
    gff_records = parse_gff(args.gff)
    extract_gene_seqs(fasta_dict, gff_records, args.output)


if __name__ == "__main__":
    main()
