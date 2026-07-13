"""
Seed script to populate books with realistic PKR prices and image URLs
Run this script to add books to the database
"""
from app import create_app
from app.models import db
from app.models.Book import Book
from app.models.Author import Author
from app.models.Category import Category
import uuid
import random

def get_books_data():
    """Returns a comprehensive list of books with author names, categories, realistic PKR prices and image URLs"""
    return [
        # Fantasy
        {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "category": "Fantasy", "price": 1299, "stock": 50, "isbn": "9780747532699", "description": "The first book in the Harry Potter series, following young wizard Harry Potter's first year at Hogwarts.", "image_url": "https://covers.openlibrary.org/b/isbn/9780747532699-L.jpg"},
        {"title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "category": "Fantasy", "price": 1299, "stock": 45, "isbn": "9780747538493", "description": "Harry's second year at Hogwarts is marked by mysterious attacks and an ancient chamber.", "image_url": "https://covers.openlibrary.org/b/isbn/9780747538493-L.jpg"},
        {"title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "category": "Fantasy", "price": 1399, "stock": 40, "isbn": "9780747542155", "description": "Harry learns about his past while being hunted by an escaped prisoner.", "image_url": "https://covers.openlibrary.org/b/isbn/9780747542155-L.jpg"},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy", "price": 1599, "stock": 60, "isbn": "9780547928227", "description": "Bilbo Baggins' unexpected journey to help reclaim the dwarves' treasure.", "image_url": "https://covers.openlibrary.org/b/isbn/9780547928227-L.jpg"},
        {"title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "category": "Fantasy", "price": 1899, "stock": 35, "isbn": "9780544003415", "description": "The first part of The Lord of the Rings trilogy, beginning Frodo's quest.", "image_url": "https://covers.openlibrary.org/b/isbn/9780544003415-L.jpg"},
        {"title": "The Two Towers", "author": "J.R.R. Tolkien", "category": "Fantasy", "price": 1899, "stock": 30, "isbn": "9780544003422", "description": "The second part of The Lord of the Rings, following the divided fellowship.", "image_url": "https://covers.openlibrary.org/b/isbn/9780544003422-L.jpg"},
        {"title": "A Game of Thrones", "author": "George R.R. Martin", "category": "Fantasy", "price": 2099, "stock": 55, "isbn": "9780553593716", "description": "The first book in A Song of Ice and Fire series, a tale of honor, intrigue, and survival.", "image_url": "https://covers.openlibrary.org/b/isbn/9780553593716-L.jpg"},
        {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "category": "Fantasy", "price": 1799, "stock": 42, "isbn": "9780756404741", "description": "The tale of Kvothe, a legendary figure telling his own story.", "image_url": "https://covers.openlibrary.org/b/isbn/9780756404741-L.jpg"},
        {"title": "The Way of Kings", "author": "Brandon Sanderson", "category": "Fantasy", "price": 2199, "stock": 38, "isbn": "9780765326355", "description": "Epic fantasy beginning The Stormlight Archive series.", "image_url": "https://covers.openlibrary.org/b/isbn/9780765326355-L.jpg"},
        {"title": "Mistborn: The Final Empire", "author": "Brandon Sanderson", "category": "Fantasy", "price": 1699, "stock": 44, "isbn": "9780765350381", "description": "A world where ash falls from the sky and evil has won.", "image_url": "https://covers.openlibrary.org/b/isbn/9780765350381-L.jpg"},
        
        # Science Fiction
        {"title": "The Martian", "author": "Andy Weir", "category": "Science Fiction", "price": 1649, "stock": 65, "isbn": "9780553418026", "description": "An astronaut's struggle to survive alone on Mars.", "image_url": "https://covers.openlibrary.org/b/isbn/9780553418026-L.jpg"},
        {"title": "Ready Player One", "author": "Ernest Cline", "category": "Science Fiction", "price": 1599, "stock": 58, "isbn": "9780307887443", "description": "A virtual reality treasure hunt in a dystopian future.", "image_url": "https://covers.openlibrary.org/b/isbn/9780307887443-L.jpg"},
        {"title": "Foundation", "author": "Isaac Asimov", "category": "Science Fiction", "price": 1449, "stock": 40, "isbn": "9780553293357", "description": "The first novel in the Foundation series about the fall and rise of galactic civilization.", "image_url": "https://covers.openlibrary.org/b/isbn/9780553293357-L.jpg"},
        {"title": "Dune", "author": "Frank Herbert", "category": "Science Fiction", "price": 2029, "stock": 48, "isbn": "9780441172719", "description": "Epic science fiction on the desert planet Arrakis.", "image_url": "https://covers.openlibrary.org/b/isbn/9780441172719-L.jpg"},
        {"title": "1984", "author": "George Orwell", "category": "Science Fiction", "price": 1199, "stock": 70, "isbn": "9780451524935", "description": "A dystopian social science fiction novel and cautionary tale.", "image_url": "https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg"},
        {"title": "Brave New World", "author": "Aldous Huxley", "category": "Science Fiction", "price": 1269, "stock": 52, "isbn": "9780060850524", "description": "A futuristic society where humans are genetically bred and pharmaceutically controlled.", "image_url": "https://covers.openlibrary.org/b/isbn/9780060850524-L.jpg"},
        {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "category": "Science Fiction", "price": 1079, "stock": 75, "isbn": "9780345391803", "description": "A comedic science fiction series following Arthur Dent's cosmic adventures.", "image_url": "https://covers.openlibrary.org/b/isbn/9780345391803-L.jpg"},
        
        # Mystery & Thriller
        {"title": "The Da Vinci Code", "author": "Dan Brown", "category": "Mystery", "price": 1779, "stock": 62, "isbn": "9780307474278", "description": "A mystery thriller following symbologist Robert Langdon.", "image_url": "https://covers.openlibrary.org/b/isbn/9780307474278-L.jpg"},
        {"title": "Angels & Demons", "author": "Dan Brown", "category": "Mystery", "price": 1719, "stock": 48, "isbn": "9780671027360", "description": "Robert Langdon's first adventure involving the Illuminati.", "image_url": "https://covers.openlibrary.org/b/isbn/9780671027360-L.jpg"},
        {"title": "Murder on the Orient Express", "author": "Agatha Christie", "category": "Mystery", "price": 1399, "stock": 55, "isbn": "9780062693662", "description": "Hercule Poirot investigates a murder on a snowbound train.", "image_url": "https://covers.openlibrary.org/b/isbn/9780062693662-L.jpg"},
        {"title": "And Then There Were None", "author": "Agatha Christie", "category": "Mystery", "price": 1329, "stock": 50, "isbn": "9780062073488", "description": "Ten strangers are invited to an island where they are murdered one by one.", "image_url": "https://covers.openlibrary.org/b/isbn/9780062073488-L.jpg"},
        {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "category": "Mystery", "price": 1839, "stock": 45, "isbn": "9780307454546", "description": "A journalist and hacker investigate a decades-old disappearance.", "image_url": "https://covers.openlibrary.org/b/isbn/9780307454546-L.jpg"},
        {"title": "Gone Girl", "author": "Gillian Flynn", "category": "Thriller", "price": 1649, "stock": 68, "isbn": "9780307588371", "description": "A psychological thriller about a marriage gone terribly wrong.", "image_url": "https://covers.openlibrary.org/b/isbn/9780307588371-L.jpg"},
        {"title": "The Girl on the Train", "author": "Paula Hawkins", "category": "Thriller", "price": 1599, "stock": 60, "isbn": "9781594633669", "description": "A psychological thriller told from three women's perspectives.", "image_url": "https://covers.openlibrary.org/b/isbn/9781594633669-L.jpg"},
        
        # Horror
        {"title": "The Shining", "author": "Stephen King", "category": "Horror", "price": 1719, "stock": 54, "isbn": "9780307743657", "description": "A family's nightmare in an isolated, haunted hotel.", "image_url": "https://covers.openlibrary.org/b/isbn/9780307743657-L.jpg"},
        {"title": "It", "author": "Stephen King", "category": "Horror", "price": 1899, "stock": 48, "isbn": "9781501142970", "description": "A group of friends face an evil entity that appears as a clown.", "image_url": "https://covers.openlibrary.org/b/isbn/9781501142970-L.jpg"},
        {"title": "Pet Sematary", "author": "Stephen King", "category": "Horror", "price": 1649, "stock": 42, "isbn": "9780743412285", "description": "A burial ground with the power to raise the dead.", "image_url": "https://covers.openlibrary.org/b/isbn/9780743412285-L.jpg"},
        {"title": "Dracula", "author": "Bram Stoker", "category": "Horror", "price": 1139, "stock": 65, "isbn": "9780486411095", "description": "The classic vampire novel that started it all.", "image_url": "https://covers.openlibrary.org/b/isbn/9780486411095-L.jpg"},
        
        # Classics
        {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "Classics", "price": 1019, "stock": 80, "isbn": "9780141439518", "description": "A romantic novel of manners set in Georgian England.", "image_url": "https://covers.openlibrary.org/b/isbn/9780141439518-L.jpg"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Classics", "price": 1199, "stock": 72, "isbn": "9780061120084", "description": "A novel about racial injustice in the American South.", "image_url": "https://covers.openlibrary.org/b/isbn/9780061120084-L.jpg"},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classics", "price": 1079, "stock": 68, "isbn": "9780743273565", "description": "A critique of the American Dream set in the Jazz Age.", "image_url": "https://covers.openlibrary.org/b/isbn/9780743273565-L.jpg"},
        {"title": "Moby-Dick", "author": "Herman Melville", "category": "Classics", "price": 1269, "stock": 45, "isbn": "9780142437247", "description": "Captain Ahab's obsessive quest for the white whale.", "image_url": "https://covers.openlibrary.org/b/isbn/9780142437247-L.jpg"},
        {"title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "category": "Classics", "price": 949, "stock": 58, "isbn": "9780486280615", "description": "Huck Finn's adventures along the Mississippi River.", "image_url": "https://covers.openlibrary.org/b/isbn/9780486280615-L.jpg"},
        {"title": "Wuthering Heights", "author": "Emily Brontë", "category": "Classics", "price": 1079, "stock": 52, "isbn": "9780141439556", "description": "A tale of passion and revenge on the Yorkshire moors.", "image_url": "https://covers.openlibrary.org/b/isbn/9780141439556-L.jpg"},
        {"title": "Great Expectations", "author": "Charles Dickens", "category": "Classics", "price": 1139, "stock": 48, "isbn": "9780141439563", "description": "The story of Pip's journey from poverty to wealth.", "image_url": "https://covers.openlibrary.org/b/isbn/9780141439563-L.jpg"},
        {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "category": "Classics", "price": 1329, "stock": 40, "isbn": "9780486415871", "description": "A psychological thriller about guilt and redemption.", "image_url": "https://covers.openlibrary.org/b/isbn/9780486415871-L.jpg"},
        {"title": "War and Peace", "author": "Leo Tolstoy", "category": "Classics", "price": 1599, "stock": 32, "isbn": "9780199232765", "description": "Epic novel of Russian society during Napoleon's invasion.", "image_url": "https://covers.openlibrary.org/b/isbn/9780199232765-L.jpg"},
        {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "category": "Classics", "price": 1019, "stock": 55, "isbn": "9780141439570", "description": "A philosophical novel about vanity and moral corruption.", "image_url": "https://covers.openlibrary.org/b/isbn/9780141439570-L.jpg"},
        
        # Young Adult
        {"title": "The Hunger Games", "author": "Suzanne Collins", "category": "Young Adult", "price": 1459, "stock": 85, "isbn": "9780439023481", "description": "A dystopian novel about a deadly televised competition.", "image_url": "https://covers.openlibrary.org/b/isbn/9780439023481-L.jpg"},
        {"title": "Catching Fire", "author": "Suzanne Collins", "category": "Young Adult", "price": 1459, "stock": 75, "isbn": "9780439023498", "description": "The second book in The Hunger Games trilogy.", "image_url": "https://covers.openlibrary.org/b/isbn/9780439023498-L.jpg"},
        {"title": "Divergent", "author": "Veronica Roth", "category": "Young Adult", "price": 1399, "stock": 68, "isbn": "9780062024039", "description": "A dystopian society divided into factions based on virtues.", "image_url": "https://covers.openlibrary.org/b/isbn/9780062024039-L.jpg"},
        {"title": "The Fault in Our Stars", "author": "John Green", "category": "Young Adult", "price": 1269, "stock": 90, "isbn": "9780142424179", "description": "A love story between two cancer patients.", "image_url": "https://covers.openlibrary.org/b/isbn/9780142424179-L.jpg"},
        {"title": "The Lightning Thief", "author": "Rick Riordan", "category": "Young Adult", "price": 1199, "stock": 78, "isbn": "9780786838653", "description": "Percy Jackson discovers he's a demigod and goes on a quest.", "image_url": "https://covers.openlibrary.org/b/isbn/9780786838653-L.jpg"},
        {"title": "City of Bones", "author": "Cassandra Clare", "category": "Young Adult", "price": 1329, "stock": 64, "isbn": "9781416914280", "description": "A girl discovers a world of Shadowhunters and demons.", "image_url": "https://covers.openlibrary.org/b/isbn/9781416914280-L.jpg"},
        {"title": "Eleanor & Park", "author": "Rainbow Rowell", "category": "Young Adult", "price": 1139, "stock": 58, "isbn": "9781250012579", "description": "A love story about two star-crossed misfits.", "image_url": "https://covers.openlibrary.org/b/isbn/9781250012579-L.jpg"},
        
        # Contemporary Fiction
        {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction", "price": 1079, "stock": 95, "isbn": "9780062315007", "description": "A shepherd's journey to find a treasure and his destiny.", "image_url": "https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg"},
        {"title": "The Kite Runner", "author": "Khaled Hosseini", "category": "Fiction", "price": 1519, "stock": 72, "isbn": "9781594631931", "description": "A story of friendship and redemption set in Afghanistan.", "image_url": "https://covers.openlibrary.org/b/isbn/9781594631931-L.jpg"},
        {"title": "A Thousand Splendid Suns", "author": "Khaled Hosseini", "category": "Fiction", "price": 1599, "stock": 68, "isbn": "9781594489501", "description": "Two women's lives intertwine in Taliban-ruled Afghanistan.", "image_url": "https://covers.openlibrary.org/b/isbn/9781594489501-L.jpg"},
        {"title": "The Book Thief", "author": "Markus Zusak", "category": "Historical Fiction", "price": 1399, "stock": 76, "isbn": "9780375842207", "description": "Death narrates a story of a girl in Nazi Germany.", "image_url": "https://covers.openlibrary.org/b/isbn/9780375842207-L.jpg"},
        {"title": "All the Light We Cannot See", "author": "Anthony Doerr", "category": "Historical Fiction", "price": 1719, "stock": 65, "isbn": "9781476746586", "description": "A blind French girl and German boy's lives collide in WWII.", "image_url": "https://covers.openlibrary.org/b/isbn/9781476746586-L.jpg"},
        {"title": "The Nightingale", "author": "Kristin Hannah", "category": "Historical Fiction", "price": 1649, "stock": 70, "isbn": "9780312577223", "description": "Two sisters' struggle to survive in occupied France.", "image_url": "https://covers.openlibrary.org/b/isbn/9780312577223-L.jpg"},
        {"title": "Little Fires Everywhere", "author": "Celeste Ng", "category": "Fiction", "price": 1599, "stock": 62, "isbn": "9780735224292", "description": "Intertwined fates of two families in suburban Ohio.", "image_url": "https://covers.openlibrary.org/b/isbn/9780735224292-L.jpg"},
        {"title": "The Handmaid's Tale", "author": "Margaret Atwood", "category": "Dystopian", "price": 1519, "stock": 68, "isbn": "9780385490818", "description": "A dystopian novel about a totalitarian theocracy.", "image_url": "https://covers.openlibrary.org/b/isbn/9780385490818-L.jpg"},
        {"title": "Norwegian Wood", "author": "Haruki Murakami", "category": "Fiction", "price": 1459, "stock": 55, "isbn": "9780375704024", "description": "A nostalgic story of love and loss in 1960s Tokyo.", "image_url": "https://covers.openlibrary.org/b/isbn/9780375704024-L.jpg"},
        {"title": "Kafka on the Shore", "author": "Haruki Murakami", "category": "Fiction", "price": 1599, "stock": 48, "isbn": "9781400079278", "description": "A surreal tale of a runaway boy and an aging simpleton.", "image_url": "https://covers.openlibrary.org/b/isbn/9781400079278-L.jpg"},
        
        # Romance
        {"title": "The Notebook", "author": "Nicholas Sparks", "category": "Romance", "price": 1199, "stock": 82, "isbn": "9781455582877", "description": "An enduring love story that spans a lifetime.", "image_url": "https://covers.openlibrary.org/b/isbn/9781455582877-L.jpg"},
        {"title": "Me Before You", "author": "Jojo Moyes", "category": "Romance", "price": 1329, "stock": 74, "isbn": "9780143124542", "description": "A life-changing relationship between a caregiver and her patient.", "image_url": "https://covers.openlibrary.org/b/isbn/9780143124542-L.jpg"},
        {"title": "It Ends with Us", "author": "Colleen Hoover", "category": "Romance", "price": 1399, "stock": 88, "isbn": "9781501110368", "description": "A powerful story about breaking the cycle of abuse.", "image_url": "https://covers.openlibrary.org/b/isbn/9781501110368-L.jpg"},
        {"title": "Beach Read", "author": "Emily Henry", "category": "Romance", "price": 1269, "stock": 76, "isbn": "9781984806734", "description": "Two writers challenge each other to write in opposite genres.", "image_url": "https://covers.openlibrary.org/b/isbn/9781984806734-L.jpg"},
        {"title": "The Seven Husbands of Evelyn Hugo", "author": "Taylor Jenkins Reid", "category": "Fiction", "price": 1519, "stock": 85, "isbn": "9781501161933", "description": "A reclusive Hollywood icon tells her scandalous story.", "image_url": "https://covers.openlibrary.org/b/isbn/9781501161933-L.jpg"},
        
        # Non-Fiction
        {"title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "category": "Non-Fiction", "price": 1839, "stock": 92, "isbn": "9780062316097", "description": "A groundbreaking narrative of humanity's creation and evolution.", "image_url": "https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg"},
        {"title": "Educated", "author": "Tara Westover", "category": "Memoir", "price": 1599, "stock": 78, "isbn": "9780399590504", "description": "A memoir about a woman who leaves her survivalist family.", "image_url": "https://covers.openlibrary.org/b/isbn/9780399590504-L.jpg"},
        {"title": "Becoming", "author": "Michelle Obama", "category": "Biography", "price": 1899, "stock": 95, "isbn": "9781524763138", "description": "The memoir of former First Lady Michelle Obama.", "image_url": "https://covers.openlibrary.org/b/isbn/9781524763138-L.jpg"},
        {"title": "Steve Jobs", "author": "Walter Isaacson", "category": "Biography", "price": 2099, "stock": 68, "isbn": "9781451648539", "description": "The exclusive biography of Apple's co-founder.", "image_url": "https://covers.openlibrary.org/b/isbn/9781451648539-L.jpg"},
        
        # Philosophy
        {"title": "The Stranger", "author": "Albert Camus", "category": "Philosophy", "price": 1139, "stock": 58, "isbn": "9780679420262", "description": "An existential novel about a man who commits murder.", "image_url": "https://covers.openlibrary.org/b/isbn/9780679420262-L.jpg"},
        {"title": "Siddhartha", "author": "Hermann Hesse", "category": "Philosophy", "price": 949, "stock": 64, "isbn": "9780553208849", "description": "A spiritual journey of self-discovery.", "image_url": "https://covers.openlibrary.org/b/isbn/9780553208849-L.jpg"},
        {"title": "Meditations", "author": "Marcus Aurelius", "category": "Philosophy", "price": 819, "stock": 72, "isbn": "9780140449334", "description": "Personal writings of the Roman Emperor on Stoic philosophy.", "image_url": "https://covers.openlibrary.org/b/isbn/9780140449334-L.jpg"},
    ]

def seed_books():
    """Seed books into the database"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("Starting book seeding with PKR prices and image URLs...")
        print("=" * 60 + "\n")
        
        # Get all authors and categories
        authors = {author.author_name: author.id for author in Author.query.filter_by(is_deleted=False).all()}
        categories = {cat.category_type: cat.id for cat in Category.query.filter_by(is_deleted=False).all()}
        
        print(f"Found {len(authors)} authors and {len(categories)} categories")
        
        books_data = get_books_data()
        added_count = 0
        existing_count = 0
        skipped_count = 0
        
        for book_data in books_data:
            try:
                # Check if book already exists by ISBN or title
                existing = Book.query.filter(
                    (Book.isbn == book_data.get('isbn')) | (Book.title == book_data['title'])
                ).filter_by(is_deleted=False).first()
                
                if existing:
                    existing_count += 1
                    # Update existing book with new data
                    updated = False
                    if not existing.image_url and book_data.get('image_url'):
                        existing.image_url = book_data['image_url']
                        updated = True
                    if existing.price != book_data['price']:
                        existing.price = book_data['price']
                        updated = True
                    if existing.description != book_data.get('description', ''):
                        existing.description = book_data.get('description', '')
                        updated = True
                    if updated:
                        db.session.commit()
                        print(f"✓ Updated: {existing.title} - PKR {existing.price}")
                    continue
            except Exception as e:
                print(f"⚠ Error checking book '{book_data.get('title')}': {str(e)}")
                existing_count += 1
                db.session.rollback()
                continue
            
            # Get author and category IDs
            author_id = authors.get(book_data['author'])
            category_id = categories.get(book_data['category'])
            
            if not author_id:
                print(f"⚠ Warning: Author '{book_data['author']}' not found for book '{book_data['title']}'")
                skipped_count += 1
                continue
            
            if not category_id:
                print(f"⚠ Warning: Category '{book_data['category']}' not found for book '{book_data['title']}'")
                skipped_count += 1
                continue
            
            # Create book
            try:
                book = Book(
                    id=str(uuid.uuid4()),
                    title=book_data['title'],
                    isbn=book_data.get('isbn'),
                    price=book_data['price'],
                    stock_quantity=book_data.get('stock', random.randint(20, 100)),
                    description=book_data.get('description', ''),
                    image_url=book_data.get('image_url'),
                    author_id=author_id,
                    category_id=category_id,
                    is_active=1,
                    role=0,
                    created_by='system'
                )
                db.session.add(book)
                db.session.flush()  # Flush to catch integrity errors before commit
                added_count += 1
                print(f"✓ Added: {book.title} - PKR {book.price}")
            except Exception as e:
                db.session.rollback()
                print(f"⚠ Skipped (already exists): {book_data['title']}")
                existing_count += 1
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"⚠ Error committing books: {str(e)}")
        
        print(f"\n{'=' * 60}")
        print(f"✓ Books: {added_count} added, {existing_count} already existed, {skipped_count} skipped")
        print(f"{'=' * 60}")
        print(f"Total books in database: {Book.query.filter_by(is_deleted=False).count()}")
        print(f"{'=' * 60}\n")

if __name__ == '__main__':
    seed_books()
