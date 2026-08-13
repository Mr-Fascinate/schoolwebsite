from app import app
from models import db, User, News, Event, Page, Setting
import json
import datetime

def initialize():
    with app.app_context():
        # Create all tables in the SQLite database
        db.create_all()
        print("Database tables created successfully.")

        # Check if default admin exists, if not, create
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin_user = User(username='admin')
            admin_user.set_password('adminpassword123')
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created successfully:")
            print("  Username: admin")
            print("  Password: adminpassword123")
        else:
            print("Admin user already exists.")

        # Seed news if empty
        if News.query.count() == 0:
            sample_news = [
                News(
                    title="Admission Open for academic year 2026-27",
                    content="Admissions are now open for Nursery to Class IX and Class XI. Inquiries can be submitted online or directly at the school office. Scholarship opportunities are available for meritorious candidates.",
                    image_url="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                    date=datetime.datetime(2026, 6, 1)
                ),
                News(
                    title="Mathematics Standard vs Basic Option Details for Class X",
                    content="Class X students are advised to submit their choices for Mathematics Standard vs Basic Option form as per CBSE guidelines. Parent consultation sessions will be held this Saturday.",
                    image_url="https://images.unsplash.com/photo-1453733190148-c44698c26588?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                    date=datetime.datetime(2026, 5, 15)
                ),
                News(
                    title="Annual Function Celebrations & Cultural Showcases",
                    content="Relive the beautiful highlights of Kautilya's Annual Function featuring traditional dances, music, and student plays. The event was graced by eminent educators and artists.",
                    image_url="https://images.unsplash.com/photo-1511578314322-379afb476865?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                    date=datetime.datetime(2026, 4, 20)
                )
            ]
            db.session.add_all(sample_news)
            db.session.commit()
            print("Sample news seeded successfully.")

        # Seed events if empty
        if Event.query.count() == 0:
            sample_events = [
                Event(
                    title="Annual Athletic Meet 2026",
                    description="The biggest sporting event of the year, featuring track and field finals, inter-house relays, and the closing ceremony.",
                    location="Main Sports Arena",
                    date=datetime.datetime(2026, 10, 15, 9, 0),
                    image_url="https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
                ),
                Event(
                    title="Inter-School Debating Championship",
                    description="Welcoming top schools from across the country to debate on contemporary economic and environmental issues.",
                    location="Auditorium A",
                    date=datetime.datetime(2026, 11, 2, 10, 0),
                    image_url="https://images.unsplash.com/photo-1453733190148-c44698c26588?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
                ),
                Event(
                    title="Winter Music & Art Concert",
                    description="An evening of classical performances and a modern art exhibition showcasing the talent of our fine arts students.",
                    location="Creative Arts Center",
                    date=datetime.datetime(2026, 12, 18, 18, 0),
                    image_url="https://images.unsplash.com/photo-1511578314322-379afb476865?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"
                )
            ]
            db.session.add_all(sample_events)
            db.session.commit()
            print("Sample events seeded successfully.")

        # Seed default settings
        if not Setting.query.get('navbar_config'):
            nav_config_setting = Setting(
                key='navbar_config',
                value=json.dumps({
                    "logo_title": "KAUTILYA",
                    "logo_subtitle": "EDUCATION ACADEMY",
                    "logo_url": "",
                    "stickers": [
                        {
                            "id": "sticker_default",
                            "url": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=100",
                            "width": 45,
                            "height": 45,
                            "position": "logo-right",
                            "margin_left": 15,
                            "margin_right": 10
                        }
                    ]
                })
            )
            db.session.add(nav_config_setting)
            db.session.commit()
            print("Default navbar_config seeded.")

        if not Setting.query.get('footer_config'):
            footer_config_setting = Setting(
                key='footer_config',
                value=json.dumps({
                    "about_text": "Kautilya Education Academy (KEA) is a leading English medium CBSE-affiliated school dedicated to academic excellence, character building, and holistic growth.",
                    "address": "Kautilya Education Academy, A.B. Road (Barwal), Shajapur, Madhya Pradesh, Pin-465001",
                    "email": "kautilya.academy@rediffmail.com",
                    "phone_office": "+91 97540 36037",
                    "phone_admissions": "+91 94251 23079",
                    "copyright_text": "© 2026-27 Kautilya Education Academy, Shajapur. All rights reserved. | CBSE Affiliation No. 1030483",
                    "quick_links": [
                        {"label": "About Us", "url": "/about-us"},
                        {"label": "Admissions", "url": "/admissions"},
                        {"label": "Contact Us", "url": "/contact-us"},
                        {"label": "Jobs at Kautilya", "url": "/jobs"}
                    ]
                })
            )
            db.session.add(footer_config_setting)
            db.session.commit()
            print("Default footer_config seeded.")

        # Seed default pages if not existing
        default_pages = [
            {
                "slug": "about-us",
                "title": "About Us",
                "schema": [
                    {
                        "id": "about_s1",
                        "type": "text",
                        "content": {
                            "heading": "Our Mission",
                            "paragraph": "To nurture young minds into compassionate leaders, innovators, and thinkers who will shape a better tomorrow. We combine rigorous academic foundation with practical learning and ethical guidance."
                        }
                    },
                    {
                        "id": "about_s2",
                        "type": "text",
                        "content": {
                            "heading": "Our Vision",
                            "paragraph": "To be a global benchmark for holistic education, where values meet technology, tradition meets innovation, and every student discovers their true potential in a safe, inspiring environment."
                        }
                    },
                    {
                        "id": "about_s3",
                        "type": "text",
                        "content": {
                            "heading": "Our History & Legacy",
                            "paragraph": "KEA is a leading English medium school, affiliated to CBSE, New Delhi, under Registration No. 1030483. To guide our students toward success, we have continuously strived for advancements, innovation, and improvements, achieving rapid and widespread success.\n\nThe institute's goal is to spread a breeze of high-quality knowledge and holistic education in Central India, making Kautilya Education Academy a premier landmark institution in the Shajapur district. Our modern campus building features progressive resources and facilities to foster synergistic growth."
                        }
                    },
                    {
                        "id": "about_s4",
                        "type": "cards",
                        "content": {
                            "title": "Our Leadership",
                            "cards": [
                                {
                                    "title": "Mr. Brajesh Yadav",
                                    "description": "Chairman of Kautilya Education Academy",
                                    "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80"
                                },
                                {
                                    "title": "Mr. N.S. Dodiya",
                                    "description": "Principal of Kautilya Education Academy",
                                    "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80"
                                },
                                {
                                    "title": "Mrs. Rekha Yadav",
                                    "description": "Administrator of Kautilya Education Academy",
                                    "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80"
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "slug": "admissions",
                "title": "Admissions",
                "schema": [
                    {
                        "id": "adm_s1",
                        "type": "text",
                        "content": {
                            "heading": "Admission Process & Guidelines",
                            "paragraph": "Welcome to the Kautilya Admissions portal. We admit students from Nursery through Class XII. The process begins with an inquiry form, followed by an interactive session or aptitude assessment (for higher classes) to evaluate the child's developmental readiness."
                        }
                    },
                    {
                        "id": "adm_s2",
                        "type": "text",
                        "content": {
                            "heading": "Required Documentation",
                            "paragraph": "To complete registration, please prepare:\n1. Birth Certificate copy\n2. Transfer Certificate from the previous school (original)\n3. Previous academic marksheets\n4. Passport size photos of student and parents\n5. Aadhaar card copy"
                        }
                    }
                ]
            },
            {
                "slug": "life-at-kautilya",
                "title": "Life at Kautilya",
                "schema": [
                    {
                        "id": "life_s1",
                        "type": "text",
                        "content": {
                            "heading": "A Vibrant Student Experience",
                            "paragraph": "Life at Kautilya is rich and diverse, spanning athletics, music, debate, robotics, and social service. Our co-curricular programs complement rigorous academics, helping students find new passions."
                        }
                    },
                    {
                        "id": "life_s2",
                        "type": "gallery",
                        "content": {
                            "title": "Campus Activities & Infrastructure",
                            "images": [
                                {
                                    "url": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=600",
                                    "caption": "Creative Smart Classroom sessions"
                                },
                                {
                                    "url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600",
                                    "caption": "Students exploring science experiments"
                                },
                                {
                                    "url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600",
                                    "caption": "Inter-house sports relays"
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "slug": "events",
                "title": "Events & Celebrations",
                "schema": [
                    {
                        "id": "ev_s1",
                        "type": "text",
                        "content": {
                            "heading": "Calendar & Highlights",
                            "paragraph": "We host several academic competitions, science fairs, exhibitions, and national festival celebrations throughout the year. Keep track of current scheduled programs."
                        }
                    }
                ]
            },
            {
                "slug": "centres-of-excellence",
                "title": "Centres of Excellence",
                "schema": [
                    {
                        "id": "coe_s1",
                        "type": "text",
                        "content": {
                            "heading": "State-of-the-Art Labs & Infrastructure",
                            "paragraph": "Our school features dedicated Physics, Chemistry, Biology, and Computer Science laboratories, along with a resource-rich library containing thousands of reference books, encyclopedias, and educational subscriptions."
                        }
                    }
                ]
            },
            {
                "slug": "updates",
                "title": "Updates & Notifications",
                "schema": [
                    {
                        "id": "up_s1",
                        "type": "text",
                        "content": {
                            "heading": "Latest Announcements",
                            "paragraph": "Find recent notices, exam datesheets, and student directives published directly by the school administration."
                        }
                    }
                ]
            },
            {
                "slug": "alumni",
                "title": "Alumni Association",
                "schema": [
                    {
                        "id": "al_s1",
                        "type": "text",
                        "content": {
                            "heading": "Stay Connected",
                            "paragraph": "We take immense pride in our alumni network, who are studying in premier universities and working in leading organizations. Register to join the Kautilya Alumni Association."
                        }
                    }
                ]
            },
            {
                "slug": "jobs",
                "title": "Careers at Kautilya",
                "schema": [
                    {
                        "id": "job_s1",
                        "type": "text",
                        "content": {
                            "heading": "Join Our Faculty",
                            "paragraph": "We look for passionate, dedicated teachers and administrative professionals who are committed to mentoring students. Send your resume to our official email to apply for open vacancies."
                        }
                    }
                ]
            },
            {
                "slug": "contact-us",
                "title": "Contact Us",
                "schema": [
                    {
                        "id": "con_s1",
                        "type": "text",
                        "content": {
                            "heading": "Get in Touch",
                            "paragraph": "For inquiries regarding admissions, careers, or administrative procedures, please contact us:\n\nOffice Hours: Mon - Sat (8:30 AM - 2:00 PM)\nAddress: A.B. Road (Barwal), Shajapur, MP - 465001"
                        }
                    },
                    {
                        "id": "con_s2",
                        "type": "embed",
                        "content": {
                            "heading": "Find Us on Google Maps",
                            "url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3663.7844078864756!2d76.273187!3d23.278385!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39634e320f78a2e7%3A0xe54d6fae1f7dcf0b!2sKautilya%20Education%20Academy!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin",
                            "height": 450,
                            "width": "100%",
                            "autoplay": False
                        }
                    }
                ]
            }
        ]

        for p_data in default_pages:
            existing_p = Page.query.filter_by(slug=p_data['slug']).first()
            if not existing_p:
                new_p = Page(
                    title=p_data['title'],
                    slug=p_data['slug'],
                    schema_json=json.dumps(p_data['schema'])
                )
                db.session.add(new_p)
                db.session.commit()
                print(f"Default page /{p_data['slug']} seeded successfully.")

if __name__ == '__main__':
    initialize()
