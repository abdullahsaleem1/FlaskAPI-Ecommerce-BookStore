"""
Seed script to populate categories and authors
Run this script to add default categories and authors to the database
"""
from app import create_app
from app.models import db
from app.models.Category import Category
from app.models.Author import Author
import uuid

def seed_categories():
    """Seed default book categories"""
    categories = [
        'Fiction',
        'Non-Fiction',
        'Science Fiction',
        'Fantasy',
        'Mystery',
        'Thriller',
        'Romance',
        'Horror',
        'Biography',
        'History',
        'Science',
        'Technology',
        'Self-Help',
        'Business',
        'Children',
        'Young Adult',
        'Poetry',
        'Drama',
        'Cooking',
        'Travel',
        'Philosophy',
        'Religion',
        'Psychology',
        'Art',
        'Music',
        'Sports',
        'Health & Fitness',
        'Politics',
        'Economics',
        'Law',
        'Medical',
        'Education',
        'Nature',
        'Comics & Graphic Novels',
        'True Crime',
        'Memoir',
        'Essay',
        'Anthology',
        'Classics',
        'Contemporary',
        'Historical Fiction',
        'Adventure',
        'Action',
        'Dystopian',
        'Paranormal',
        'Crime',
        'Western',
        'Satire',
        'Humor',
        'Reference'
    ]
    
    added_count = 0
    existing_count = 0
    
    for category_type in categories:
        existing = Category.query.filter_by(category_type=category_type, is_deleted=False).first()
        
        if existing:
            existing_count += 1
            continue
        
        category = Category(
            id=str(uuid.uuid4()),
            category_type=category_type,
            is_active=1,
            role=0,
            created_by='system'
        )
        db.session.add(category)
        added_count += 1
    
    db.session.commit()
    
    print(f"[INFO] Categories: {added_count} added, {existing_count} already existed")
    return added_count

def seed_authors():
    """Seed default authors"""
    authors = [
        'J.K. Rowling',
        'Stephen King',
        'Agatha Christie',
        'J.R.R. Tolkien',
        'George R.R. Martin',
        'Dan Brown',
        'Paulo Coelho',
        'Harper Lee',
        'Ernest Hemingway',
        'Jane Austen',
        'Mark Twain',
        'Charles Dickens',
        'Leo Tolstoy',
        'F. Scott Fitzgerald',
        'Gabriel García Márquez',
        'Isaac Asimov',
        'Arthur Conan Doyle',
        'H.G. Wells',
        'Oscar Wilde',
        'Virginia Woolf',
        'George Orwell',
        'Franz Kafka',
        'James Joyce',
        'Margaret Atwood',
        'Haruki Murakami',
        'Neil Gaiman',
        'Terry Pratchett',
        'Brandon Sanderson',
        'Patrick Rothfuss',
        'Rick Riordan',
        'Suzanne Collins',
        'Veronica Roth',
        'Cassandra Clare',
        'John Green',
        'Rainbow Rowell',
        'Leigh Bardugo',
        'Sarah J. Maas',
        'V.E. Schwab',
        'Tomi Adeyemi',
        'Erin Morgenstern',
        'Lois Lowry',
        'Orson Scott Card',
        'Ray Bradbury',
        'Kurt Vonnegut',
        'Aldous Huxley',
        'Philip K. Dick',
        'Ursula K. Le Guin',
        'Douglas Adams',
        'C.S. Lewis',
        'Tolkien',
        'Homer',
        'Dante Alighieri',
        'William Shakespeare',
        'Emily Dickinson',
        'Edgar Allan Poe',
        'Fyodor Dostoevsky',
        'Anton Chekhov',
        'Hermann Hesse',
        'Albert Camus',
        'Jean-Paul Sartre',
        'Simone de Beauvoir',
        'Toni Morrison',
        'Maya Angelou',
        'James Baldwin',
        'Chinua Achebe',
        'Chimamanda Ngozi Adichie',
        'Khaled Hosseini',
        'Yaa Gyasi',
        'Celeste Ng',
        'Jhumpa Lahiri',
        'Amy Tan',
        'Kazuo Ishiguro',
        'Salman Rushdie',
        'Zadie Smith',
        'Isabel Allende',
        'Laura Esquivel',
        'Octavia Butler',
        'N.K. Jemisin',
        'Ted Chiang',
        'Andy Weir',
        'Ernest Cline',
        'Blake Crouch',
        'Gillian Flynn',
        'Paula Hawkins',
        'Ruth Ware',
        'Tana French',
        'Michael Connelly',
        'Lee Child',
        'David Baldacci',
        'John Grisham',
        'James Patterson',
        'Nora Roberts',
        'Nicholas Sparks',
        'Colleen Hoover',
        'Emily Henry',
        'Taylor Jenkins Reid',
        'Fredrik Backman',
        'Kristin Hannah',
        'Jodi Picoult'
    ]
    
    added_count = 0
    existing_count = 0
    
    for author_name in authors:
        existing = Author.query.filter_by(author_name=author_name, is_deleted=False).first()
        
        if existing:
            existing_count += 1
            continue
        
        author = Author(
            id=str(uuid.uuid4()),
            author_name=author_name,
            is_active=1,
            role=0,
            created_by='system'
        )
        db.session.add(author)
        added_count += 1
    
    db.session.commit()
    
    print(f"[INFO] Authors: {added_count} added, {existing_count} already existed")
    return added_count

def seed_data():
    """Main seeding function"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("Starting database seeding...")
        print("=" * 60 + "\n")
        
        categories_added = seed_categories()
        authors_added = seed_authors()
        
        print("\n" + "=" * 60)
        print("[INFO] Database seeding completed successfully!")
        print("=" * 60)
        print(f"Total items added: {categories_added + authors_added}")
        print("=" * 60 + "\n")

if __name__ == '__main__':
    seed_data()
