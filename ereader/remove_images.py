# filepath: /Users/dan.popa/work/ereader-swedish/remove_images.py
import panflute as pf

def remove_images(elem, doc):
    if isinstance(elem, pf.Image):
        return []

def main(doc=None):
    return pf.run_filter(remove_images, doc=doc)

if __name__ == "__main__":
    main()