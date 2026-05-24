# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 34: Vector Databases (Local Search with ChromaDB)
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - What is a Vector Database and why traditional SQL/NoSQL databases fail RAG
    - Introducing ChromaDB: A lightweight, open-source vector store
    - Creating collections, adding documents, and generating auto-embeddings
    - Querying vector databases for Top-K semantic matching
    - Filtering results dynamically using metadata logic

  Why this matters for AI:
    In a standard database, searching for "errors" won't find a record containing
    the word "bug" or "failure" unless you do complex keyword mappings.
    Vector Databases store semantic concepts. When you query for "database crash",
    ChromaDB instantly locates documents discussing "Postgres database connection timeout"
    using geometric math, enabling highly precise context retrieval for your LLMs.

  Estimated time: 25 minutes

===============================================================================
"""

import sys

# === UNDERSTANDING VECTOR DATABASES =========================================
#
# WHAT IS A VECTOR DATABASE?
#   Imagine a traditional SQL database like an organized spreadsheet: you look up rows using strict keywords,
#   like finding an employee by their ID number. A Vector Database is like an art gallery where paintings
#   are grouped by theme. There are no tables or row numbers; instead, paintings are placed in 3D rooms:
#   landscapes in one room, portraits in another. When you bring a photo of a tree (a query vector), the
#   gallery assistant instantly shows you the paintings in the landscape room because they share the same
#   visual theme (semantic coordinates)!
#   (Vectors and Embeddings explained fully in Module 5, Lesson 3 — "Chunking Strategies & Vector Embeddings")
#
# WHAT IS A VECTOR INDEX AND ANN?
#   - A Vector Index is a structured path map through our language galaxy map. Instead of calculating the
#     exact Cosine Similarity distance to all 10 million documents in the database (which would be incredibly
#     slow), the index organizes vectors into clusters, acting like highways and local roads.
#   - Approximate Nearest Neighbor (ANN) is the shortcut search algorithm we use to travel this index map.
#     It doesn't guarantee finding the absolute, 100% closest matching star in the entire universe, but it
#     guarantees finding a 99.9% close match in 2 milliseconds instead of 5 minutes!
#
# Traditional Databases (Postgres, MongoDB):
#   - Store rows, columns, and JSON documents.
#   - Search via exact keyword matching (index indexes, text match).
#   - Fail at semantic queries (e.g. searching "happy" won't return "joyful").
#
# Vector Databases (ChromaDB, Pinecone, Milvus):
#   - Store text chunks alongside their multi-dimensional float arrays (embeddings).
#   - Index using HNSW (Hierarchical Navigable Small World) algorithms for fast search.
#   - Search via geometric proximity (e.g. nearest neighbors).

# print("--- 1. SEMANTIC SEARCH VS. KEYWORD SEARCH ---")
print("  Query: 'API Routing'")
print("  Keyword Match: 'No exact matches found.'")
print("  Vector DB Match: Found 'FastAPI path decorations' (Similarity: 88.5%)")


# === SAFE CHROMADB IMPORT & MOCK FALLBACK ===================================
#
# To make this lesson 100% self-contained and runnable immediately, we will
# attempt to import `chromadb`. If it is missing, we fall back to a beautiful,
# in-memory Mock Client that implements the EXACT same API syntax in pure Python!

try:
    import chromadb
    chromadb_installed = True
    print("\n[INFO] Native ChromaDB imported successfully.")
except ImportError:
    chromadb_installed = False
    print("\n[INFO] ChromaDB not installed. Using premium In-Memory Mock Vector Store...")
    
    # Let's build a gorgeous mock that mirrors the real ChromaDB API:
    class MockCollection:
        def __init__(self, name):
            self.name = name
            self.docs = []
            self.metadata = []
            self.ids = []
            
        def add(self, ids, documents, metadatas=None):
            self.ids.extend(ids)
            self.documents = documents if hasattr(self, 'documents') else []
            self.documents.extend(documents)
            if metadatas:
                self.metadata.extend(metadatas)
            else:
                self.metadata.extend([{} for _ in documents])
                
        def query(self, query_texts, n_results=2, where=None):
            results = {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }
            
            # Simple keyword overlap scoring as mock similarity
            query_word = query_texts[0].lower().split()[0] if query_texts[0].split() else ""
            scored_docs = []
            
            for idx, doc in enumerate(self.documents):
                # Filter metadata if where condition exists
                if where:
                    skip = False
                    for k, v in where.items():
                        if self.metadata[idx].get(k) != v:
                            skip = True
                    if skip:
                        continue
                        
                score = 0.9 if query_word in doc.lower() else 0.2
                scored_docs.append((score, self.ids[idx], doc, self.metadata[idx]))
                
            # Sort by score descending (top-k)
            scored_docs.sort(reverse=True, key=lambda x: x[0])
            
            for score, cid, doc, meta in scored_docs[:n_results]:
                results["ids"][0].append(cid)
                results["documents"][0].append(doc)
                results["metadatas"][0].append(meta)
                results["distances"][0].append(1.0 - score)
                
            return results

    class MockClient:
        def __init__(self):
            self.collections = {}
            
        def create_collection(self, name):
            self.collections[name] = MockCollection(name)
            return self.collections[name]
            
        def get_or_create_collection(self, name):
            if name not in self.collections:
                self.collections[name] = MockCollection(name)
            return self.collections[name]


# === ORCHESTRATING CHROMADB OPERATIONS =======================================
#
# Whether using real ChromaDB or our mock fallback, the syntax is identical!
# Let's initialize the database, seed it with document chunks, and query it.

# print("\n--- 2. SEEDING THE VECTOR STORE COLLECTION ---")

# 1. Instantiate the Client
if chromadb_installed:
    # Use real in-memory SQLite store
    client = chromadb.Client()
else:
    client = MockClient()

# 2. Create the Collection (like creating a SQL table)
collection = client.get_or_create_collection("company_manual")

# 3. Seed documentation chunks
kb_documents = [
    "FastAPI is a Python web framework. It hosts routes on port 8000.",
    "CORS middleware must be configured to allow React frontend connection access.",
    "ChromaDB stores document text chunks alongside their float vectors for similarity queries.",
    "Docker containers package native dependencies and run identically in production.",
    "Git merge conflicts occur when same lines are edited concurrently on distinct branches."
]

kb_metadatas = [
    {"category": "api", "difficulty": "intermediate"},
    {"category": "api", "difficulty": "intermediate"},
    {"category": "database", "difficulty": "advanced"},
    {"category": "devops", "difficulty": "intermediate"},
    {"category": "git", "difficulty": "beginner"}
]

kb_ids = [f"id_{idx}" for idx in range(1, len(kb_documents) + 1)]

# Add to database
collection.add(
    ids=kb_ids,
    documents=kb_documents,
    metadatas=kb_metadatas
)
print(f"Successfully created and seeded collection '{collection.name}' with {len(kb_documents)} items.")


# === EXECUTING VECTOR QUERIES & METADATA FILTERING ===========================
#
# We perform semantic queries using `.query()`.
# We can also restrict search bounds using the `where` parameter (metadata filtering).

# print("\n--- 3. EXECUTING SEMANTIC VECTOR QUERIES ---")

query_str = "How do I fix browser blocking in my web app?"
print(f"Querying Database for: '{query_str}'")

results = collection.query(
    query_texts=[query_str],
    n_results=2
)

# Print matches
print("\nTop-2 Semantic Match Results:")
for idx in range(len(results["ids"][0])):
    match_id = results["ids"][0][idx]
    doc = results["documents"][0][idx]
    meta = results["metadatas"][0][idx]
    dist = results["distances"][0][idx]
    
    print(f"  Match #{idx+1} (ID: {match_id}) [Distance: {dist:.4f}]:")
    print(f"    Text: {doc}")
    print(f"    Metadata: {meta}")

# --- Metadata Filtering ---
# print("\n--- 4. METADATA FILTERED QUERIES ---")
print("Searching for 'Python' but restricting to category='database':")

filtered_results = collection.query(
    query_texts=["Python"],
    n_results=1,
    where={"category": "database"} # Strict category lock!
)

print(f"  Matched Doc: {filtered_results['documents'][0][0]}")
print(f"  Metadata: {filtered_results['metadatas'][0][0]}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Overwriting collections on server restarts
#   By default, `chromadb.Client()` creates a transient in-memory database.
#   Every time your python script exits, all data is lost.
#   In development, use `chromadb.PersistentClient(path="./chroma_db")` to persist
#   the files to disk in a local folder.

# MISTAKE 2: Unfiltered retrieval returning irrelevant modules
#   If you search for "security keys" across the entire database, you might retrieve
#   user accounts documentation instead of AWS configuration settings.
#   Always enrich document chunks with rich metadata tags (category, file_path, tags)
#   and use the `where` filter to narrow search contexts.

# MISTAKE 3: Bulk upload without batching
#   Attempting to upload 50,000 PDF document chunks in a single `.add()` call can crash
#   system memory limits. Always slice large seed datasets into small batches (e.g. 500 records)
#   when writing database migrations.


# === EXERCISES ================================================================
#
# Exercise 1: In our MockCollection, expand the `add` method to raise a ValueError
#             if the length of `ids` does not match the length of `documents`.
#
# Exercise 2: Contrast named volume mounts (used to persist ChromaDB folders inside
#             Docker Compose containers) vs transient inside-container storage.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # (Inside MockCollection class):
# # if len(ids) != len(documents):
# #     raise ValueError("Length of ids and documents must match.")


# === KEY TAKEAWAYS ============================================================
#
# - Vector databases specialize in rapid, high-dimensional similarity queries.
# - ChromaDB offers a developer-first, local SQLite-based persistent store.
# - Collections act as index partitions that segregate unrelated document domains.
# - Adding records triggers automatic text-embedding generation at database boundaries.
# - Metadata filtering (where) combines keyword boundaries with semantic proximity.
