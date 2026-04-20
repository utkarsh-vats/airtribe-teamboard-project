from django.core.management.base import BaseCommand
from api.models import KBEntry


class Command(BaseCommand):
    help = 'Seed the knowledge base with sample entries'

    def handle(self, *args, **options):
        if KBEntry.objects.exists():
            self.stdout.write(self.style.WARNING('Knowledge base already seeded. Skipping.'))
            return

        entries = [
            {
                'question': 'What is select_related in Django ORM?',
                'answer': 'select_related performs a SQL JOIN and fetches related objects in a single query. Use it for ForeignKey and OneToOneField relationships to avoid the N+1 query problem.',
                'category': 'database',
            },
            {
                'question': 'What is prefetch_related in Django ORM?',
                'answer': 'prefetch_related performs a separate lookup for each relationship and does the joining in Python. Use it for ManyToManyField and reverse ForeignKey relationships. Unlike select_related, it uses separate queries.',
                'category': 'database',
            },
            {
                'question': 'How does transaction.atomic() work in Django?',
                'answer': 'transaction.atomic() wraps a block of code in a database transaction. If any exception is raised inside the block, all changes are rolled back. If the block completes successfully, the transaction is committed.',
                'category': 'database',
            },
            {
                'question': 'What are Q objects in Django?',
                'answer': 'Q objects allow you to build complex lookups using OR (|), AND (&), and NOT (~) operators. They are useful when you need to combine multiple conditions that cannot be expressed with simple keyword arguments in filter().',
                'category': 'framework',
            },
            {
                'question': 'What is a JWT token and how does it work?',
                'answer': 'JWT (JSON Web Token) is a compact, URL-safe token format used for authentication. It contains three parts: header, payload, and signature. The server generates a token on login and the client sends it with subsequent requests to prove identity.',
                'category': 'api',
            },
            {
                'question': 'How do Django signals work?',
                'answer': 'Django signals allow decoupled applications to get notified when certain actions occur. Common signals include post_save and pre_save. You write a receiver function, connect it to a signal using the @receiver decorator, and wire it in AppConfig.ready().',
                'category': 'framework',
            },
            {
                'question': 'What are REST API best practices?',
                'answer': 'Key REST API best practices include using proper HTTP methods (GET, POST, PUT, DELETE), returning appropriate status codes, versioning your API, using pagination for large datasets, and authenticating requests with tokens.',
                'category': 'api',
            },
            {
                'question': 'What is Amazon EC2?',
                'answer': 'Amazon EC2 (Elastic Compute Cloud) provides resizable virtual servers in the cloud. You can choose instance types based on CPU, memory, and storage needs. EC2 supports auto-scaling and integrates with other AWS services like S3 and RDS.',
                'category': 'cloud',
            },
            {
                'question': 'What are S3 buckets in AWS?',
                'answer': 'Amazon S3 (Simple Storage Service) buckets are containers for storing objects (files) in the cloud. S3 offers high durability, availability, and scalability. Common use cases include static file hosting, backups, and data lakes.',
                'category': 'cloud',
            },
            {
                'question': 'What is Django middleware?',
                'answer': 'Middleware is a framework of hooks into Django request/response processing. Each middleware component processes requests before they reach the view and responses before they reach the client. Common uses include authentication, CORS handling, and logging.',
                'category': 'framework',
            },
            {
                'question': 'How does PostgreSQL indexing improve performance?',
                'answer': 'PostgreSQL indexes create a data structure that allows the database to find rows faster without scanning the entire table. B-tree indexes are the default and work well for equality and range queries. Use indexes on columns frequently used in WHERE, JOIN, and ORDER BY clauses.',
                'category': 'database',
            },
            {
                'question': 'What is the difference between authentication and authorization?',
                'answer': 'Authentication verifies who a user is (identity), typically via credentials like username and password. Authorization determines what an authenticated user is allowed to do (permissions). In Django REST Framework, authentication is handled by authentication classes and authorization by permission classes.',
                'category': 'general',
            },
        ]

        for entry in entries:
            KBEntry.objects.create(**entry)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(entries)} knowledge base entries.'))