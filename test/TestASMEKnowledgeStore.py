from db.ASMEKnowledgeStore import ASMEKnowledgeStore

pdf_path_1 = "../test/data/marvel_prop_auction.pdf"
pdf_path_2 = "../test/data/golf_guidebook.pdf"

index_name = "asme-bot-knowledge"

query = "How much is the Elektra Natchios’ Overcoat and Pair of Stunt Wakizashis listed for?"
query2 = "What did Shot Scope find about golfers who missed their tee shots to the right?"

vectordb = ASMEKnowledgeStore(index_name)
# print(vectordb.similarity_search(query))
# print(vectordb.similarity_search(query2))

# print(vectordb.add_docs([pdf_path_2]))
# print(vectordb.similarity_search(query2))
# vectordb.clear_db()
