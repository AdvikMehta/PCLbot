from db.ASMEKnowledgeStore import ASMEKnowledgeStore

pdf_path_1 = "../test/data/marvel_prop_auction.pdf"
pdf_path_2 = "../test/data/golf_guidebook.pdf"

asme_pdf = "../test/data/2014_ASME_B31.3.pdf"

index_name = "asme-bot-knowledge"

query = "According to ASME B31.3, what is the minimum design metal temperature (in °F) for carbon steel without impact testing?"

# vectordb = ASMEKnowledgeStore(index_name, init_doc_paths=[asme_pdf])
# print(vectordb.similarity_search(query))
# print(vectordb.similarity_search(query2))

# print(vectordb.add_docs([pdf_path_2]))
# print(vectordb.similarity_search(query2))
# vectordb.clear_db()
