from db.ASMEKnowledgeStore import ASMEKnowledgeStore

pdf_path_1 = "../test/data/marvel_prop_auction.pdf"
pdf_path_2 = "../test/data/golf_guidebook.pdf"

asme_pdf = "../test/data/2014_ASME_B31.3.pdf"
asme_guide = "../test/data/asmeb313_guide.pdf"

index_name = "asme-bot-knowledge"
query = "Flanged connections should be minimized and only used when required for component and equipment connections."

vectordb = ASMEKnowledgeStore(index_name)
print(vectordb.similarity_search(query))

# print(vectordb.add_docs([asme_pdf, asme_guide]))
# vectordb.clear_db()
