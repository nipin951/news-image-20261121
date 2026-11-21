"""Hands in the entry: copies the finished news image to /output/entry.png.

The image itself (entry.png beside this file) sums up the world news of Saturday
21 November 2026. Standard library only; outside the grader, MAKEFUN_OUTPUT_DIR
stands in for /output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"), os.path.join(OUT, "entry.png"))
