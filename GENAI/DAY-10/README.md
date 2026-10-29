# DAY-10 Document Q&A

This Streamlit app indexes PDFs from `pdfdoc/` and `data/` in the same Astra DB collection used by the DAY-10 notebook. New PDFs can be saved into `data/` from the sidebar, then indexed with the **Index documents** button. Indexing uses stable document IDs and does not clear the collection, so running it again updates matching chunks instead of wiping existing data.

## Setup

From the repository root, install the app dependencies:

```bash
python -m pip install -r GENAI/DAY-10/requirements.txt
```

Set these variables in the repository-root `.env` file or `GENAI/DAY-10/.env`:

```dotenv
OPENAI_API_KEY=...
ASTRA_DB_API_ENDPOINT=...
ASTRA_DB_APPLICATION_TOKEN=...
```

The Astra credentials must have access to the `astradb_vetcor_collections` collection. Do not commit `.env` files.

## Run

From the repository root:

```bash
streamlit run GENAI/DAY-10/app.py
```

Upload PDFs in the sidebar and save them to `data/`. Click **Index documents** after adding new files. Then ask questions in the chat input. Each answer includes the retrieved PDF source and page references.

The document upload button currently accepts PDF files. PDFs already present in `pdfdoc/` are indexed along with PDFs saved in `data/`.
