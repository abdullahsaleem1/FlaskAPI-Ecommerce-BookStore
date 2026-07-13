"""
Seed script to populate books
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
    """Returns a comprehensive list of books with author names and categories"""
    return [
        # Fantasy
        {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "category": "Fantasy", "price": 19.99, "stock": 50, "isbn": "9780747532699", "description": "The first book in the Harry Potter series, following young wizard Harry Potter's first year at Hogwarts."},
        {"title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "category": "Fantasy", "price": 19.99, "stock": 45, "isbn": "9780747538493", "description": "Harry's second year at Hogwarts is marked by mysterious attacks and an ancient chamber."},
        {"title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "category": "Fantasy", "price": 21.99, "stock": 40, "isbn": "9780747542155", "description": "Harry learns about his past while being hunted by an escaped prisoner."},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fantasy", "price": 24.99, "stock": 60, "isbn": "9780547928227", "description": "Bilbo Baggins' unexpected journey to help reclaim the dwarves' treasure."},
        {"title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "category": "Fantasy", "price": 29.99, "stock": 35, "isbn": "9780544003415", "description": "The first part of The Lord of the Rings trilogy, beginning Frodo's quest."},
        {"title": "The Two Towers", "author": "J.R.R. Tolkien", "category": "Fantasy", "price": 29.99, "stock": 30, "isbn": "9780544003422", "description": "The second part of The Lord of the Rings, following the divided fellowship."},
        {"title": "A Game of Thrones", "author": "George R.R. Martin", "category": "Fantasy", "price": 32.99, "stock": 55, "isbn": "9780553593716", "description": "The first book in A Song of Ice and Fire series, a tale of honor, intrigue, and survival."},
        {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "category": "Fantasy", "price": 27.99, "stock": 42, "isbn": "9780756404741", "description": "The tale of Kvothe, a legendary figure telling his own story."},
        {"title": "The Way of Kings", "author": "Brandon Sanderson", "category": "Fantasy", "price": 34.99, "stock": 38, "isbn": "9780765326355", "description": "Epic fantasy beginning The Stormlight Archive series."},
        {"title": "Mistborn: The Final Empire", "author": "Brandon Sanderson", "category": "Fantasy", "price": 26.99, "stock": 44, "isbn": "9780765350381", "description": "A world where ash falls from the sky and evil has won."},
        
        # Science Fiction
        {"title": "The Martian", "author": "Andy Weir", "category": "Science Fiction", "price": 25.99, "stock": 65, "isbn": "9780553418026", "description": "An astronaut's struggle to survive alone on Mars."},
        {"title": "Ready Player One", "author": "Ernest Cline", "category": "Science Fiction", "price": 24.99, "stock": 58, "isbn": "9780307887443", "description": "A virtual reality treasure hunt in a dystopian future."},
        {"title": "Foundation", "author": "Isaac Asimov", "category": "Science Fiction", "price": 22.99, "stock": 40, "isbn": "9780553293357", "description": "The first novel in the Foundation series about the fall and rise of galactic civilization."},
        {"title": "Dune", "author": "Frank Herbert", "category": "Science Fiction", "price": 31.99, "stock": 48, "isbn": "9780441172719", "description": "Epic science fiction on the desert planet Arrakis."},
        {"title": "1984", "author": "George Orwell", "category": "Science Fiction", "price": 18.99, "stock": 70, "isbn": "9780451524935", "description": "A dystopian social science fiction novel and cautionary tale."},
        {"title": "Brave New World", "author": "Aldous Huxley", "category": "Science Fiction", "price": 19.99, "stock": 52, "isbn": "9780060850524", "description": "A futuristic society where humans are genetically bred and pharmaceutically controlled."},
        {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "category": "Science Fiction", "price": 16.99, "stock": 75, "isbn": "9780345391803", "description": "A comedic science fiction series following Arthur Dent's cosmic adventures."},
        
        # Mystery & Thriller
        {"title": "The Da Vinci Code", "author": "Dan Brown", "category": "Mystery", "price": 27.99, "stock": 62, "isbn": "9780307474278", "description": "A mystery thriller following symbologist Robert Langdon."},
        {"title": "Angels & Demons", "author": "Dan Brown", "category": "Mystery", "price": 26.99, "stock": 48, "isbn": "9780671027360", "description": "Robert Langdon's first adventure involving the Illuminati."},
        {"title": "Murder on the Orient Express", "author": "Agatha Christie", "category": "Mystery", "price": 21.99, "stock": 55, "isbn": "9780062693662", "description": "Hercule Poirot investigates a murder on a snowbound train."},
        {"title": "And Then There Were None", "author": "Agatha Christie", "category": "Mystery", "price": 20.99, "stock": 50, "isbn": "9780062073488", "description": "Ten strangers are invited to an island where they are murdered one by one."},
        {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "category": "Mystery", "price": 28.99, "stock": 45, "isbn": "9780307454546", "description": "A journalist and hacker investigate a decades-old disappearance."},
        {"title": "Gone Girl", "author": "Gillian Flynn", "category": "Thriller", "price": 25.99, "stock": 68, "isbn": "9780307588371", "description": "A psychological thriller about a marriage gone terribly wrong."},
        {"title": "The Girl on the Train", "author": "Paula Hawkins", "category": "Thriller", "price": 24.99, "stock": 60, "isbn": "9781594633669", "description": "A psychological thriller told from three women's perspectives."},
        
        # Horror
        {"title": "The Shining", "author": "Stephen King", "category": "Horror", "price": 26.99, "stock": 54, "isbn": "9780307743657", "description": "A family's nightmare in an isolated, haunted hotel."},
        {"title": "It", "author": "Stephen King", "category": "Horror", "price": 29.99, "stock": 48, "isbn": "9781501142970", "description": "A group of friends face an evil entity that appears as a clown."},
        {"title": "Pet Sematary", "author": "Stephen King", "category": "Horror", "price": 25.99, "stock": 42, "isbn": "9780743412285", "description": "A burial ground with the power to raise the dead."},
        {"title": "Dracula", "author": "Bram Stoker", "category": "Horror", "price": 17.99, "stock": 65, "isbn": "9780486411095", "description": "The classic vampire novel that started it all."},
        
        # Classics
        {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "Classics", "price": 15.99, "stock": 80, "isbn": "9780141439518", "description": "A romantic novel of manners set in Georgian England."},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Classics", "price": 18.99, "stock": 72, "isbn": "9780061120084", "description": "A novel about racial injustice in the American South."},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classics", "price": 16.99, "stock": 68, "isbn": "9780743273565", "description": "A critique of the American Dream set in the Jazz Age."},
        {"title": "Moby-Dick", "author": "Herman Melville", "category": "Classics", "price": 19.99, "stock": 45, "isbn": "9780142437247", "description": "Captain Ahab's obsessive quest for the white whale."},
        {"title": "The Adventures of Huckleberry Finn", "author": "Mark Twain", "category": "Classics", "price": 14.99, "stock": 58, "isbn": "9780486280615", "description": "Huck Finn's adventures along the Mississippi River."},
        {"title": "Wuthering Heights", "author": "Emily Brontë", "category": "Classics", "price": 16.99, "stock": 52, "isbn": "9780141439556", "description": "A tale of passion and revenge on the Yorkshire moors."},
        {"title": "Great Expectations", "author": "Charles Dickens", "category": "Classics", "price": 17.99, "stock": 48, "isbn": "9780141439563", "description": "The story of Pip's journey from poverty to wealth."},
        {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "category": "Classics", "price": 20.99, "stock": 40, "isbn": "9780486415871", "description": "A psychological thriller about guilt and redemption."},
        {"title": "War and Peace", "author": "Leo Tolstoy", "category": "Classics", "price": 24.99, "stock": 32, "isbn": "9780199232765", "description": "Epic novel of Russian society during Napoleon's invasion."},
        {"title": "The Picture of Dorian Gray", "author": "Oscar Wilde", "category": "Classics", "price": 15.99, "stock": 55, "isbn": "9780141439570", "description": "A philosophical novel about vanity and moral corruption."},
        
        # Young Adult
        {"title": "The Hunger Games", "author": "Suzanne Collins", "category": "Young Adult", "price": 22.99, "stock": 85, "isbn": "9780439023481", "description": "A dystopian novel about a deadly televised competition."},
        {"title": "Catching Fire", "author": "Suzanne Collins", "category": "Young Adult", "price": 22.99, "stock": 75, "isbn": "9780439023498", "description": "The second book in The Hunger Games trilogy."},
        {"title": "Divergent", "author": "Veronica Roth", "category": "Young Adult", "price": 21.99, "stock": 68, "isbn": "9780062024039", "description": "A dystopian society divided into factions based on virtues."},
        {"title": "The Fault in Our Stars", "author": "John Green", "category": "Young Adult", "price": 19.99, "stock": 90, "isbn": "9780142424179", "description": "A love story between two cancer patients."},
        {"title": "The Lightning Thief", "author": "Rick Riordan", "category": "Young Adult", "price": 18.99, "stock": 78, "isbn": "9780786838653", "description": "Percy Jackson discovers he's a demigod and goes on a quest."},
        {"title": "City of Bones", "author": "Cassandra Clare", "category": "Young Adult", "price": 20.99, "stock": 64, "isbn": "9781416914280", "description": "A girl discovers a world of Shadowhunters and demons."},
        {"title": "Eleanor & Park", "author": "Rainbow Rowell", "category": "Young Adult", "price": 17.99, "stock": 58, "isbn": "9781250012579", "description": "A love story about two star-crossed misfits."},
        
        # Contemporary Fiction
        {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction", "price": 16.99, "stock": 95, "isbn": "9780062315007", "description": "A shepherd's journey to find a treasure and his destiny."},
        {"title": "The Kite Runner", "author": "Khaled Hosseini", "category": "Fiction", "price": 23.99, "stock": 72, "isbn": "9781594631931", "description": "A story of friendship and redemption set in Afghanistan."},
        {"title": "A Thousand Splendid Suns", "author": "Khaled Hosseini", "category": "Fiction", "price": 24.99, "stock": 68, "isbn": "9781594489501", "description": "Two women's lives intertwine in Taliban-ruled Afghanistan."},
        {"title": "The Book Thief", "author": "Markus Zusak", "category": "Historical Fiction", "price": 21.99, "stock": 76, "isbn": "9780375842207", "description": "Death narrates a story of a girl in Nazi Germany."},
        {"title": "All the Light We Cannot See", "author": "Anthony Doerr", "category": "Historical Fiction", "price": 26.99, "stock": 65, "isbn": "9781476746586", "description": "A blind French girl and German boy's lives collide in WWII."},
        {"title": "The Nightingale", "author": "Kristin Hannah", "category": "Historical Fiction", "price": 25.99, "stock": 70, "isbn": "9780312577223", "description": "Two sisters' struggle to survive in occupied France."},
        {"title": "Little Fires Everywhere", "author": "Celeste Ng", "category": "Fiction", "price": 24.99, "stock": 62, "isbn": "9780735224292", "description": "Intertwined fates of two families in suburban Ohio."},
        {"title": "The Handmaid's Tale", "author": "Margaret Atwood", "category": "Dystopian", "price": 23.99, "stock": 68, "isbn": "9780385490818", "description": "A dystopian novel about a totalitarian theocracy."},
        {"title": "Norwegian Wood", "author": "Haruki Murakami", "category": "Fiction", "price": 22.99, "stock": 55, "isbn": "9780375704024", "description": "A nostalgic story of love and loss in 1960s Tokyo."},
        {"title": "Kafka on the Shore", "author": "Haruki Murakami", "category": "Fiction", "price": 24.99, "stock": 48, "isbn": "9781400079278", "description": "A surreal tale of a runaway boy and an aging simpleton."},
        
        # Romance
        {"title": "The Notebook", "author": "Nicholas Sparks", "category": "Romance", "price": 18.99, "stock": 82, "isbn": "9781455582877", "description": "An enduring love story that spans a lifetime."},
        {"title": "Me Before You", "author": "Jojo Moyes", "category": "Romance", "price": 20.99, "stock": 74, "isbn": "9780143124542", "description": "A life-changing relationship between a caregiver and her patient."},
        {"title": "It Ends with Us", "author": "Colleen Hoover", "category": "Romance", "price": 21.99, "stock": 88, "isbn": "9781501110368", "description": "A powerful story about breaking the cycle of abuse."},
        {"title": "Beach Read", "author": "Emily Henry", "category": "Romance", "price": 19.99, "stock": 76, "isbn": "9781984806734", "description": "Two writers challenge each other to write in opposite genres."},
        {"title": "The Seven Husbands of Evelyn Hugo", "author": "Taylor Jenkins Reid", "category": "Fiction", "price": 23.99, "stock": 85, "isbn": "9781501161933", "description": "A reclusive Hollywood icon tells her scandalous story."},
        
        # Non-Fiction
        {"title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "category": "Non-Fiction", "price": 28.99, "stock": 92, "isbn": "9780062316097", "description": "A groundbreaking narrative of humanity's creation and evolution."},
        {"title": "Educated", "author": "Tara Westover", "category": "Memoir", "price": 24.99, "stock": 78, "isbn": "9780399590504", "description": "A memoir about a woman who leaves her survivalist family."},
        {"title": "Becoming", "author": "Michelle Obama", "category": "Biography", "price": 29.99, "stock": 95, "isbn": "9781524763138", "description": "The memoir of former First Lady Michelle Obama."},
        {"title": "Steve Jobs", "author": "Walter Isaacson", "category": "Biography", "price": 32.99, "stock": 68, "isbn": "9781451648539", "description": "The exclusive biography of Apple's co-founder."},
        
        # Philosophy
        {"title": "The Stranger", "author": "Albert Camus", "category": "Philosophy", "price": 17.99, "stock": 58, "isbn": "9780679420262", "description": "An existential novel about a man who commits murder."},
        {"title": "Siddhartha", "author": "Hermann Hesse", "category": "Philosophy", "price": 14.99, "stock": 64, "isbn": "9780553208849", "description": "A spiritual journey of self-discovery."},
        {"title": "Being and Nothingness", "author": "Jean-Paul Sartre", "category": "Philosophy", "price": 26.99, "stock": 35, "isbn": "9780671867805", "description": "A foundational text of existentialism."},
        
        # Comics & Graphic Novels
        {"title": "Watchmen", "author": "Alan Moore", "category": "Comics & Graphic Novels", "price": 29.99, "stock": 52, "isbn": "9781401245252", "description": "A groundbreaking graphic novel that redefined the medium."},
        {"title": "The Sandman Vol. 1", "author": "Neil Gaiman", "category": "Comics & Graphic Novels", "price": 24.99, "stock": 58, "isbn": "9781401284770", "description": "Dream, the lord of dreams, is captured and seeks revenge."},
        {"title": "American Gods", "author": "Neil Gaiman", "category": "Fantasy", "price": 27.99, "stock": 62, "isbn": "9780062572233", "description": "Old gods clash with new in modern America."},
        {"title": "Good Omens", "author": "Neil Gaiman", "category": "Fantasy", "price": 25.99, "stock": 56, "isbn": "9780060853983", "description": "An angel and demon team up to prevent the apocalypse."},
        
        # Poetry & Drama
        {"title": "The Complete Poems", "author": "Emily Dickinson", "category": "Poetry", "price": 22.99, "stock": 42, "isbn": "9780316184137", "description": "The complete collection of Emily Dickinson's poems."},
        {"title": "The Complete Tales and Poems", "author": "Edgar Allan Poe", "category": "Poetry", "price": 24.99, "stock": 48, "isbn": "9780394716787", "description": "The complete works of Edgar Allan Poe."},
        {"title": "Hamlet", "author": "William Shakespeare", "category": "Drama", "price": 12.99, "stock": 75, "isbn": "9780743477123", "description": "The tragedy of the Prince of Denmark."},
        {"title": "Romeo and Juliet", "author": "William Shakespeare", "category": "Drama", "price": 11.99, "stock": 80, "isbn": "9780743477116", "description": "The world's most famous love story."},
        
        # Children's
        {"title": "The Chronicles of Narnia", "author": "C.S. Lewis", "category": "Children", "price": 34.99, "stock": 65, "isbn": "9780066238500", "description": "The complete series of the magical land of Narnia."},
        {"title": "Charlotte's Web", "author": "E.B. White", "category": "Children", "price": 12.99, "stock": 88, "isbn": "9780064400558", "description": "A pig and spider's unlikely friendship."},
        {"title": "Where the Wild Things Are", "author": "Maurice Sendak", "category": "Children", "price": 15.99, "stock": 92, "isbn": "9780060254926", "description": "Max's imaginative journey to where the wild things are."},
    ]

def seed_books():
    """Seed books into the database"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("Starting book seeding...")
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
            # Check if book already exists
            existing = Book.query.filter_by(title=book_data['title'], is_deleted=False).first()
            if existing:
                existing_count += 1
                continue
            
            # Get author and category IDs
            author_id = authors.get(book_data['author'])
            category_id = categories.get(book_data['category'])
            
            if not author_id:
                print(f"[Warning]: Author '{book_data['author']}' not found for book '{book_data['title']}'")
                skipped_count += 1
                continue
            
            if not category_id:
                print(f"⚠ Warning: Category '{book_data['category']}' not found for book '{book_data['title']}'")
                skipped_count += 1
                continue
            
            # Create book
            book = Book(
                id=str(uuid.uuid4()),
                title=book_data['title'],
                isbn=book_data.get('isbn'),
                price=book_data['price'],
                stock_quantity=book_data.get('stock', random.randint(20, 100)),
                description=book_data.get('description', ''),
                author_id=author_id,
                category_id=category_id,
                is_active=1,
                role=0,
                created_by='system'
            )
            db.session.add(book)
            added_count += 1
        
        db.session.commit()
        
        print(f"\n✓ Books: {added_count} added, {existing_count} already existed, {skipped_count} skipped")
        print("\n" + "=" * 60)
        print("[INFO] Book seeding completed successfully!")
        print("=" * 60)
        print(f"Total books in database: {Book.query.filter_by(is_deleted=False).count()}")
        print("=" * 60 + "\n")

if __name__ == '__main__':
    seed_books()
