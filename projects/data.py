import random
from datetime import date, timedelta
from django.contrib.auth.models import User
from projects.models import Project, Category, ProjectImage
from django.core.files.base import ContentFile
import io
from PIL import Image

def populate_dummy_data():
    # 1. Create some dummy categories
    category_names = ["Web Development", "Data Science", "Mobile App", "Game Development", "AI/ML"]
    categories = []

    for name in category_names:
        category, _ = Category.objects.get_or_create(name=name)
        categories.append(category)

    # 2. Get or create some dummy users
    users = list(User.objects.all())
    if len(users) < 10:
        for i in range(10 - len(users)):
            user = User.objects.create_user(
                username=f'user{i}', 
                email=f'user{i}@example.com', 
                password='password123'
            )
            users.append(user)

    # 3. Generate 50 dummy projects
    for i in range(50):
        title = f"Project {i+1}"
        category = random.choice(categories)
        start_date = date.today() - timedelta(days=random.randint(10, 300))
        end_date = start_date + timedelta(days=random.randint(30, 120))
        skills = random.sample(["Python", "Django", "React", "Node.js", "ML", "CSS", "HTML", "PostgreSQL"], 3)
        contributors = random.sample(users, random.randint(1, 3))
        status = random.choice(['draft', 'published', 'completed'])

        project = Project.objects.create(
            title=title,
            description=f"Description for {title}",
            category=category,
            start_date=start_date,
            end_date=end_date,
            skills_need=", ".join(skills),
            publish_date=end_date,
            live_link=f"https://example.com/project-{i+1}" if status != "draft" else "",
            status=status,
        )
        project.contributor.set(contributors)

        # 4. Add a dummy image
        img = Image.new("RGB", (100, 100), color=(
            random.randint(0, 255), 
            random.randint(0, 255), 
            random.randint(0, 255)
        ))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        image_file = ContentFile(buf.getvalue(), f"project_image_{i+1}.png")

        ProjectImage.objects.create(project=project, image=image_file)

    print("✅ 50 dummy project entries added successfully.")

