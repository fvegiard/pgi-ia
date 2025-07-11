#!/usr/bin/env python3
"""
parse_directive.py  CLI pour extraire les données d'une directive PDF

Usage:
  python parse_directive.py path/to/directive.pdf
"""
import sys
import json
import asyncio
from pathlib import Path

try:
    from backend.agents.directive_agent import DirectiveAgent
except ImportError:
    print("Erreur: module backend.agents.directive_agent introuvable.")
    sys.exit(1)


async def main(pdf_path: Path):
    agent = DirectiveAgent()
    result = await agent.process_directive(pdf_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    pdf_file = Path(sys.argv[1])
    if not pdf_file.exists():
        print(f"Fichier non trouvé: {pdf_file}")
        sys.exit(1)
    asyncio.run(main(pdf_file))