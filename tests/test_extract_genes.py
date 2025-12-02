import os
import tempfile

import pytest

from extract_genes import (
    load_fasta,
    parse_gff,
    extract_gene_seqs,
)


def write_tmp_file(content: str, suffix: str = "") -> str:
    fh = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=suffix, encoding="utf-8")
    fh.write(content)
    fh.close()
    return fh.name


def test_load_fasta_basic():
    fasta = ">chr1\nATGCATGCATGC\n>plasmidA desc\nGGGAAATTT\n"
    p = write_tmp_file(fasta, suffix=".fasta")
    seqs = load_fasta(p)
    os.unlink(p)
    assert "chr1" in seqs
    assert seqs["chr1"] == "ATGCATGCATGC"
    assert seqs["plasmidA"] == "GGGAAATTT"


def test_parse_gff_and_extract_plus_strand(tmp_path):
    fasta = ">chr1\nAAAAACCCCGGGGTTTT\n"
    gff = "chr1\tsource\tgene\t2\t5\t.\t+\t.\tID=gene1;Name=testgene\n"
    fa = tmp_path / "g.fasta"
    gf = tmp_path / "g.gff"
    out = tmp_path / "out.fna"
    fa.write_text(fasta)
    gf.write_text(gff)
    seqs = load_fasta(str(fa))
    recs = parse_gff(str(gf))
    extract_gene_seqs(seqs, recs, str(out))
    content = out.read_text()
    assert ">testgene" in content
    # coords 2-5 => positions 2..5 in 1-based (inclusive): slice [1:5] = AAAA
    assert "AAAA" in content  # basic containment check


def test_extract_minus_strand(tmp_path):
    fasta = ">chr1\nATGCGTAC\n"
    # gene from 1 to 3 on minus strand => subseq ATG -> rc = CAT
    gff = "chr1\tsrc\tgene\t1\t3\t.\t-\t.\tID=g1;Name=g1\n"
    fa = tmp_path / "f.fasta"
    gf = tmp_path / "f.gff"
    out = tmp_path / "o.fna"
    fa.write_text(fasta)
    gf.write_text(gff)
    seqs = load_fasta(str(fa))
    recs = parse_gff(str(gf))
    extract_gene_seqs(seqs, recs, str(out))
    content = out.read_text()
    assert ">g1" in content
    assert "CAT" in content  # reverse complement of ATG


def test_invalid_seqid_raises(tmp_path):
    fasta = ">chr1\nATGC\n"
    gff = "chrX\tsrc\tgene\t1\t2\t.\t+\t.\tID=x\n"
    fa = tmp_path / "a.fasta"
    gf = tmp_path / "a.gff"
    fa.write_text(fasta)
    gf.write_text(gff)
    seqs = load_fasta(str(fa))
    recs = parse_gff(str(gf))
    with pytest.raises(ValueError):
        extract_gene_seqs(seqs, recs, str(tmp_path / "out.fna"))


def test_coords_out_of_range(tmp_path):
    fasta = ">c1\nATGC\n"
    gff = "c1\tsrc\tgene\t1\t10\t.\t+\t.\tID=big\n"
    fa = tmp_path / "b.fasta"
    gf = tmp_path / "b.gff"
    fa.write_text(fasta)
    gf.write_text(gff)
    seqs = load_fasta(str(fa))
    recs = parse_gff(str(gf))
    with pytest.raises(ValueError):
        extract_gene_seqs(seqs, recs, str(tmp_path / "out.fna"))
