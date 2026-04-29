# 🎮 Metacritic Data Scraper

Um scraper robusto para coleta e análise de dados do Metacritic, desenvolvido em Python.  
O projeto automatiza a extração de notas da crítica e do público, calcula a divergência entre elas (_Gap_) e exporta os resultados em múltiplos formatos.

---

## 🚀 Funcionalidades

### ✨ Extração Paralela

Utiliza `ThreadPoolExecutor` para executar múltiplas instâncias do navegador simultaneamente, aumentando significativamente a performance.

### 🧹 Processamento de Dados

- Limpeza automática de strings
- Normalização de URLs
- Estruturação eficiente com Pandas

### 📊 Cálculo de Gap

Determina a diferença absoluta entre:

- Nota da crítica especializada
- Nota dos usuários
- graficos e insights usando dados adquiridos 

### 📁 Exportação Multiformato

Suporte para geração de relatórios em:

- Excel
- CSV
- JSON
- HTML

---

## 🛠️ Tecnologias Utilizadas

- 🐍 Python 3.x
- 🌐 Selenium
- 📊 Pandas
- 📈 XlsxWriter
- ⚡ Concurrent Futures

---

## 📁 Estrutura do Projeto

```bash
metacritic-scraper/
├── pipeline.py        # Orquestra o fluxo da aplicação
├── scraping.py        # Lógica de raspagem e automação
├── arquivazacao.py    # Implementação do padrão Factory
├── salvamentos/       # Relatórios gerados
```
