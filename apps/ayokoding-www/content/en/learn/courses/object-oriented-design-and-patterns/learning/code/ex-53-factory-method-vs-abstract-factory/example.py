"""Example 53: Factory Method vs Abstract Factory, Contrasted on One Example."""

import abc  # => imports the abc module


class Document(abc.ABC):  # => the ONE product FACTORY METHOD varies
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def kind(self) -> str:  # => no body -- required by every concrete document
        ...  # => the ellipsis stub -- concrete documents below fill this in


class PdfDocument(Document):  # => a CONCRETE product
    def kind(self) -> str:  # => defines the kind() method
        return "pdf"  # => returns this value to the caller


class WordDocument(Document):  # => a DIFFERENT concrete product, same axis of variation
    def kind(self) -> str:  # => defines the kind() method
        return "word"  # => returns this value to the caller


# => FACTORY METHOD: varies WHICH single product a creator method returns
class DocumentCreator(abc.ABC):  # => each subclass overrides ONE creation method
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def create_document(self) -> Document:  # => no body -- required by every creator
        ...  # => the ellipsis stub -- concrete creators below fill this in

    def open_document(self) -> str:  # => the shared, NON-varying workflow around creation
        doc: Document = self.create_document()  # => the ONE varying step, deferred to subclasses
        return f"opened a {doc.kind()} document"  # => returns this value to the caller


class PdfCreator(DocumentCreator):  # => varies WHICH product create_document() returns
    def create_document(self) -> Document:  # => defines the create_document() method
        return PdfDocument()  # => returns this value to the caller


class WordCreator(DocumentCreator):  # => varies WHICH product create_document() returns
    def create_document(self) -> Document:  # => defines the create_document() method
        return WordDocument()  # => returns this value to the caller


# => ABSTRACT FACTORY: varies WHICH FAMILY of several related products are produced TOGETHER
class Toolbar(abc.ABC):  # => a SECOND product kind that must MATCH the chosen Document family
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def kind(self) -> str:  # => no body -- required by every concrete toolbar
        ...  # => the ellipsis stub -- concrete toolbars below fill this in


class PdfToolbar(Toolbar):  # => belongs to the SAME family as PdfDocument
    def kind(self) -> str:  # => defines the kind() method
        return "pdf-toolbar"  # => returns this value to the caller


class WordToolbar(Toolbar):  # => belongs to the SAME family as WordDocument
    def kind(self) -> str:  # => defines the kind() method
        return "word-toolbar"  # => returns this value to the caller


class SuiteFactory(abc.ABC):  # => produces a MATCHED (Document, Toolbar) pair, together
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def create_document(self) -> Document:  # => no body -- required by every suite
        ...  # => the ellipsis stub -- concrete suites below fill this in

    @abc.abstractmethod  # => marks the next method as required for every subclass
    def create_toolbar(self) -> Toolbar:  # => no body -- required by every suite
        ...  # => the ellipsis stub -- concrete suites below fill this in


class PdfSuiteFactory(SuiteFactory):  # => produces ONLY the PDF family, matched together
    def create_document(self) -> Document:  # => defines the create_document() method
        return PdfDocument()  # => returns this value to the caller

    def create_toolbar(self) -> Toolbar:  # => defines the create_toolbar() method
        return PdfToolbar()  # => returns this value to the caller


factory_method_result: str = PdfCreator().open_document()  # => varies ONE product
print(factory_method_result)  # => Factory Method solved "which single Document to build"
# => Output: opened a pdf document

suite: SuiteFactory = PdfSuiteFactory()  # => varies an ENTIRE matched family at once
family: tuple[str, str] = (
    suite.create_document().kind(),
    suite.create_toolbar().kind(),
)  # => BOTH products come from the SAME family, guaranteed
print(family)  # => Abstract Factory solved "which matched FAMILY of products to build"
# => Output: ('pdf', 'pdf-toolbar')
# => Factory Method varies ONE product; Abstract Factory varies a whole FAMILY of related products together
