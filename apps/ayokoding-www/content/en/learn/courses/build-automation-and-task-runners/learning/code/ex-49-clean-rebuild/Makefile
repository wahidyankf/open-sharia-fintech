# artifact.txt is a file target made from source.txt.
artifact.txt: source.txt
	cp $< $@

.PHONY: clean
clean:
	rm -f artifact.txt
