import wikipedia

wikipedia.set_lang("en")

try:
    results = wikipedia.search("Jr. NTR")
    print("Search results:", results)

    if results:
        print(wikipedia.summary(results[0], sentences=3))

except Exception as e:
    print("Wikipedia error:", repr(e))