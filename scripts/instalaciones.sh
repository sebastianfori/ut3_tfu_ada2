#!/usr/bin/env bash
set -e

echo "==========================================="
echo " Instalador de jq y xmlstarlet para Git Bash"
echo " (sin permisos de administrador)"
echo "==========================================="

BIN="$HOME/bin"
mkdir -p "$BIN"

echo ""
echo "=== Instalando jq ==="
curl -L -o "$BIN/jq.exe" \
  https://github.com/stedolan/jq/releases/download/jq-1.6/jq-win64.exe
chmod +x "$BIN/jq.exe"
echo "jq instalado en $BIN/jq.exe"

echo ""
echo "=== Instalando xmlstarlet (reemplazo de xmllint) ==="
curl -L -o "$BIN/xml.exe" \
  https://downloads.sourceforge.net/project/xmlstar/xmlstarlet/xmlstarlet-1.6.1/xmlstarlet-1.6.1-win32.zip

TMP="/tmp/xml"
rm -rf "$TMP"
mkdir -p "$TMP"

unzip -q "$BIN/xml.exe" -d "$TMP"
cp "$TMP/xmlstarlet-1.6.1-win32/xml.exe" "$BIN/xml.exe"
chmod +x "$BIN/xml.exe"

rm -rf "$TMP"
echo "xmlstarlet instalado en $BIN/xml.exe"

echo ""
echo "=== Agregando $HOME/bin al PATH si no está ==="
if ! grep -q 'export PATH="$HOME/bin:$PATH"' "$HOME/.bashrc"; then
  echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
  echo "Línea agregada al .bashrc"
else
  echo "Ya estaba en el PATH"
fi

echo ""
echo "==========================================="
echo " Instalación completa."
echo "==========================================="
