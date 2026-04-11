We are building a complete, responsive frontend for an event management website for https://gbf.org.ly/.
The backend is already fully built and stable. I will describe the pages one by one, including:
•	The purpose of each page
•	All required API endpoints
•	Request body (if any)
•	Expected response structure
•	Any authentication requirements
Requirements:
•	The frontend must be fully responsive (mobile-first design + excellent laptop/desktop view)
•	Support the collars and the icon like https://gbf.org.ly/.
•	Use modern React (or Next.js if you prefer) with TypeScript
•	Clean, professional UI/UX design suitable for a professional organization
•	Proper state management, error handling, loading states, and authentication flow
•	Fully integrated with the provided APIs (including correct headers, tokens, error handling, etc.)
•	The final output should be a complete, production-ready frontend that works from start to end
I will provide the pages and APIs step by step. After each description, please implement the corresponding page/component with full functionality and integration.
Please start by suggesting the best tech stack and project structure, then wait for me to begin describing the first page.
We need a high-quality, well-structured, maintainable, and fully working frontend application.
We are builing a platform for event management, the users can login to the website using one login page and then can redirect nased on the roles. The system admin can add events, zones, companies, exhipetors inside the company and users (security and media stuff). And have a home page contain a detail information about the event.
the security user will login to the platform and scan the visitors qr code to check if it’s valid or not, and users and exipetors or media users can login to the platform, show there qr code. Search for company, zone and so on, add connection by scan any other visitor qr code. See the list of the connection for. The backend works with the following route http://89.167.92.67:3000/api/v1/ and the Authorization should be passed in all routes exept two routes. We will start by list all the routes below with the body and the response.
1.	http://89.167.92.67:3000/api/v1/add_user this route will be in the registration page POST method , this page will allow the normal visitor users to register to the platform. There is no need to pass the authorization in this route. The body must be like below so each field will have a text box in the registration page the job title must passed as visitor in this page there is no need to have text box for must passed from the background:
“
{
  "first_name": "moath",
  "last_name": "ali",
  "email": "moathf@ali.com",
  "password": "SecurePass123!",
  "phone": "+905343998077",
  "job_title": "visitor",
  "country": "USA",
  "company_name":"شركة الاتجاد",
  "city": "NYC"
              }
“
The response will be like below:
“
{
    "data": {
        "message": "User created successfully",
        "user": {
            "city": "NYC",
            "company_id": null,
            "company_name": "شركة الاتجاد",
            "country": "USA",
            "created_at": "2026-04-09T16:08:40.753540+00:00",
            "display_name": "moath ali",
            "email": "moathf@ali.com",
            "first_name": "moath",
            "id": "39487549-c593-458f-a852-48567ed97a48",
            "is_active": true,
            "job_title": "visitor",
            "last_name": "ali",
            "phone": "+905343998077",
            "photo_url": null,
            "roles": [
                {
                    "event_id": null,
                    "name": "visitor"
                }
            ]
        }
    },
    "status": "success"
}
“
2.	http://89.167.92.67:3000/api/v1/login this route will be used for all type of users to login into the platform POST method, there is no need to pass the authorization in this route, the body must as below example:
“
{"email": "zakariaaalyafawi@gmail.com", "password": "Abcdef@12345"} 
“
the response will be as below:
“
{
    "data": {
        "access_token": "4e61bbe4-4867-44bc-ab0e-4af0d0de023e",
        "auth_id": "None",
        "auth_provider": "email",
        "city": "None",
        "company": "None",
        "company_id": "None",
        "company_name": null,
        "country": "None",
        "created_at": "2026-03-16 15:04:16.618736+00:00",
        "deleted_at": "None",
        "display_name": "Zakaria Alyafawi",
        "email": "zakariaaalyafawi@gmail.com",
        "first_name": "Zakaria",
        "id": "1dc507d3-d390-485e-9fce-b92a77f65496",
        "is_active": "True",
        "is_blacklisted": "False",
        "job_title": "None",
        "last_name": "Alyafawi",
        "message": "Login successful",
        "phone": "None",
        "photo_url": "None",
        "roles": [
            {
                "event_id": null,
                "name": "super_admin",
                "role_id": "0d15ae32-f21e-49c6-93cf-31df47de0e76"
            }
        ],
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWRjNTA3ZDMtZDM5MC00ODVlLTlmY2UtYjkyYTc3ZjY1NDk2IiwiZXhwIjoxNzc1NzU0NzgwLCJpYXQiOjE3NzU3NTExODB9.H-ifhiqHW1bFCD1w5eE8KnJpXoyZxDik1gsqh3L46MM",
        "token_expires_at": "None",
        "token_last_rotated_at": "None",
        "updated_at": "2026-03-16 15:04:16.618736+00:00",
        "user_roles": "[<UserRoles(id=eb8ac274-1ee8-4758-8711-738b9168824e, user_id=1dc507d3-d390-485e-9fce-b92a77f65496, role_id=0d15ae32-f21e-49c6-93cf-31df47de0e76, event_id=None)>]"
    },
    "status": "success"
}
•	"super_admin"
•	"exhibitor_staff"
•	"event_admin"
•	"security"
•	"media"
•	"visitor"
the super_admin will have access to add [event, zones, companies, users] the system admin only can add event_admin
the event admin will have access to add [event, zones, companies, users] can’t add super admin.
The security user can search for zones, companies and will scan the users qr code.
The exhibitor_staff, media, and visitor users can search for zones, companies, and show there qr code, and add connections by scan others qr code.

3.	After successful login the http://89.167.92.67:3000/api/v1/qr route must be called and pass the authorization which is the token from the login POST method. The response will be a base64 image which is the qr code for the user. Which must be presented in the frontend.
the response will be as below:
“
{
    "data": {
        "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAXIAAAFyAQAAAADAX2ykAAACZUlEQVR4nO2bUYrjMAyGP60N+5jAHqBHcW8wRxrmZvFReoCF+HEhQftgO+m0lJlh0kwM0oNpq+/hByHZslxRvmLx15dwMN5444033njjH/FSzEPsQUQ8ck4ikKrvvKMe47fiUVVVgqqqjk5VRyCMi3d0eoUMR9Nv/Of4VDJUpHdK7EtUy2/i99Zj/HN4HZhFB2aBvPysHuM35sPoNNfnuGbtD+ox/lt8DWGnQALiywTxZfICoCS4vgI5mn7jP7B8eCrmtObvulSfna9a5HN8VwNcXnTA6a1ZfJvkc8MrIkIYZ8lN0uKAZOfnpnkdun8C3XTnD+MsxNOEnHfUY/xWfK3PI/norEOneSkbbq3Utv82yV+fr0K+pppKzIduWu6vJjtftcznrH0Tjw64fGsF+dP7S45j6jf+oZX87SZq6k7AUqShRN/yt2E+77Akj5yTh3DxyOvF59DK67izHuO34nPjI+EiKChCp0jsEY09QhjnjOg+eox/Ch97p2Xgyyyqoys1m+TzzEHOe+oxfiO+Jmf6g8bT5JXUL06n9U767156jN+WX+b7023/W5bc+lp/1Chfe10AOs0DhZtDtOraEx9Nv/Ef2Pr4psyKai9EmTSA5W+7/N38KNTUze6wRt/i2yx/9X4SyP1vSefk373kOKZ+4x/aWp9LV7RU5atK3dn+2zhf30/W+W8NchTJ98/Ze1j9xn+O17d+/TLLeqb+IT3Gb8vLGafEU2mHy6/ptz7gn63H+O/x9/tvV4ZIOnRLV2T7b+N8FBGRHihT3zJOgiRCGG3/bZQX+3+38cYbb7zxxu/O/wdxpOpYlXvsIQAAAABJRU5ErkJggg=="
    },
    "status": "success"
}
“
4.	For system admin the following http://89.167.92.67:3000/api/v1/dashboard will be requested in the home page which is the first page that will direct to after login or when pass into. The route method is GET and the authorization must be passed. The response as below:
“
{
    "data": {
        "attendance_daily": [
            {
                "count": 0,
                "date": "2026-04-09"
            },
            {
                "count": 0,
                "date": "2026-04-08"
            },
            {
                "count": 0,
                "date": "2026-04-07"
            },
            {
                "count": 0,
                "date": "2026-04-06"
            },
            {
                "count": 0,
                "date": "2026-04-05"
            },
            {
                "count": 0,
                "date": "2026-04-04"
            },
            {
                "count": 0,
                "date": "2026-04-03"
            }
        ],
        "scans_daily": [
            {
                "count": 0,
                "date": "2026-04-09"
            },
            {
                "count": 0,
                "date": "2026-04-08"
            },
            {
                "count": 0,
                "date": "2026-04-07"
            },
            {
                "count": 0,
                "date": "2026-04-06"
            },
            {
                "count": 0,
                "date": "2026-04-05"
            },
            {
                "count": 0,
                "date": "2026-04-04"
            },
            {
                "count": 0,
                "date": "2026-04-03"
            }
        ],
        "total_companies": 3,
        "total_events": 2,
        "total_zones": 1,
        "users_by_role": {
            "event_admin": 1,
            "exhibitor_staff": 1,
            "media": 2,
            "security": 3,
            "super_admin": 1,
            "visitor": 7
        }
    },
    "status": "success"
}

“

The data will be represented in a timeline graph for one week.

5.	When click on event page must move to event page and call the following routev http://89.167.92.67:3000/api/v1/retrieve_events the route method POST, the token must be passed in the authorization and body will be like below :
“{
"page": 1,
"limit": 20
}
“
The response will be list of event’s as below:
“
{
    "data": {
        "data": [
            {
                "created_at": "2026-03-31T21:58:32.736511+00:00",
                "description": "وصف",
                "end_date": "2027-01-01",
                "id": "295af916-9fbd-4ca4-a98e-2646952b5d8f",
                "is_published": true,
                "organizer_id": "8fbb26a1-396a-4adb-a9be-ab885abdc158",
                "organizer_name": "moazevent moazevent",
                "slug": "فعالية-معاذ",
                "start_date": "2026-01-01",
                "title": "فعالية معاذ",
                "venue": "موقع معاذ"
            },
            {
                "created_at": "2026-03-16T15:04:17.009219+00:00",
                "description": "Sample event for testing platform features.",
                "end_date": "2024-10-03",
                "id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "is_published": true,
                "organizer_id": "1dc507d3-d390-485e-9fce-b92a77f65496",
                "organizer_name": "Zakaria Alyafawi",
                "slug": "demo-event",
                "start_date": "2024-10-01",
                "title": "Demo Event 2024",
                "venue": "Demo Convention Center"
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 2
    },
    "status": "success"
}

“

all these event’s must presented in the page. 
6.	A add event button will be available to add a new event method is post. The following route http://89.167.92.67:3000/api/v1/add_events will be called to add a new event, the authorization must be passed too like all routes. The body will be like below:
“
{
  "slug": "new-event-2024",
  "title": "New Event 2024",
  "description": "Description",
  "start_date": "2024-11-01",
  "end_date": "2024-11-03",
  "venue": "New Venue",
  "organizer_id": "b91d6e1c-1143-44a3-b0eb-826bde756e12",
  "is_published": true
}“
the response will be like below:
“
{
    "data": {
        "event": {
            "created_at": "2026-04-09T16:46:26.540498+00:00",
            "description": "Description",
            "end_date": "2024-11-03",
            "id": "802bfa62-e0b8-4e08-8110-ef708b6d6c4f",
            "is_published": true,
            "organizer_id": "b91d6e1c-1143-44a3-b0eb-826bde756e12",
            "organizer_name": "moath ali",
            "slug": "new-event-2024",
            "start_date": "2024-11-01",
            "title": "New Event 2024",
            "venue": "New Venue"
        },
        "message": "Event created successfully"
    },
    "status": "success"
}
“

Regarding the organizer_id which is event_admin a list of exists event admin can be retrieved by calling http://89.167.92.67:3000/api/v1/retrieve_users and pass the authorization and the following body te method is post :
“
{
  "role_name": "event_admin"
}

“
The response will be like below:
“
{
    "data": {
        "data": [
            {
                "city": "NYC",
                "company_id": null,
                "company_name": "شركة الاتجاد",
                "country": "USA",
                "created_at": "2026-04-09T16:46:11.021312+00:00",
                "display_name": "moath ali",
                "email": "moathf@a0li.com",
                "first_name": "moath",
                "id": "b91d6e1c-1143-44a3-b0eb-826bde756e12",
                "is_active": true,
                "job_title": "event_admin",
                "last_name": "ali",
                "phone": "+9053439980677",
                "photo_url": null,
                "roles": [
                    "event_admin"
                ]
            },
            {
                "city": null,
                "company_id": null,
                "company_name": null,
                "country": null,
                "created_at": "2026-03-30T19:57:50.869991+00:00",
                "display_name": "moazevent moazevent",
                "email": "moazevent@gmail.com",
                "first_name": "moazevent",
                "id": "8fbb26a1-396a-4adb-a9be-ab885abdc158",
                "is_active": true,
                "job_title": "event_admin",
                "last_name": "moazevent",
                "phone": null,
                "photo_url": null,
                "roles": [
                    "event_admin"
                ]
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 2
    },
    "status": "success"
}
“
which is the list of users that can be the event organizer.
7.	To update event the following route can be called http://89.167.92.67:3000/api/v1/update_events the method is post, the body can be as below:
“
{
  "id": "802bfa62-e0b8-4e08-8110-ef708b6d6c4f",
  "organizer_id":"8fbb26a1-396a-4adb-a9be-ab885abdc158",
  "title": "Updated Title",
  "venue": "Updated Venue",
  "is_published": true
}
“
The id is the event id, the organizer id can be called and must call the list of users too, the title venue and the is published can be updated to.
The response as below:
“
{
    "data": {
        "event": {
            "created_at": "2026-04-09T16:46:26.540498+00:00",
            "description": "Description",
            "end_date": "2024-11-03",
            "id": "802bfa62-e0b8-4e08-8110-ef708b6d6c4f",
            "is_published": true,
            "organizer_id": "8fbb26a1-396a-4adb-a9be-ab885abdc158",
            "organizer_name": "moazevent moazevent",
            "slug": "new-event-2024",
            "start_date": "2024-11-01",
            "title": "Updated Title",
            "venue": "Updated Venue"
        },
        "message": "Event updated successfully"
    },
    "status": "success"
}
“

8.	To delete event the following route can be used with post method http://89.167.92.67:3000/api/v1/delete_events the authorization must be passed. The body as below:
“
{
  "id": "802bfa62-e0b8-4e08-8110-ef708b6d6c4f"
}
“
The response as below:
“
{
    "data": {
        "message": "Event deleted successfully"
    },
    "status": "success"
}
“
The user can move to the zones page when press o the zones. When move to the page the following route must be called to retrieve the zones.
9.	The http://89.167.92.67:3000/api/v1/retrieve_zones route will be user to retrieve the zones, the method is post, the authorization must be passed, the body as below:
“
{
  "page": 1,
  "limit": 20
}
“
the response as below:
“
{
    "data": {
        "data": [
            {
                "capacity": 500,
                "code": "zone11",
                "created_at": "2026-03-21T20:36:17.097970+00:00",
                "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "event_name": "Demo Event 2024",
                "id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
                "is_restricted": false,
                "location_x": null,
                "location_y": null,
                "name": "zone11"
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 1
    },
    "status": "success"
}
“

10.	To add zone the following route can be used http://89.167.92.67:3000api/v1/add_zone the route method is post, the otherization must be passed, the body as below:
“
{
  "event_id": " f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
  "name": "VIP Zone",
  "code": "VIP11",
  "capacity": 50,
  "is_restricted": true,
  "location_x": 10,
  "location_y": 20
}
“
The event_id must be selected from a list, the list can be retrieved from the retrieve_events route, in the list the event id will not be represented you know that the name will be represented and when pass on it the id will pass to the route from the background.the response can will be as below:
“
{
    "data": {
        "message": "Zone created successfully",
        "zone": {
            "capacity": 50,
            "code": "VIP11",
            "created_at": "2026-04-09T17:24:44.795308+00:00",
            "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
            "event_name": "Demo Event 2024",
            "id": "2eb3ee8a-9774-47cf-8bd7-8500108d011f",
            "is_restricted": true,
            "location_x": 10,
            "location_y": 20,
            "name": "VIP Zone"
        }
    },
    "status": "success"
}
“
11.	To update zone the following route can be used http://89.167.92.67:3000/api/v1/update_zone the method is post and the authorization must be passed which is the token from the login, the body as below:
“
{
  "id": "2eb3ee8a-9774-47cf-8bd7-8500108d011f",
"name": "VIP Updated",
  "capacity": 60
}
“
The response will be as below:
“
{
    "data": {
        "message": "Zone updated successfully",
        "zone": {
            "capacity": 60,
            "code": "VIP11",
            "created_at": "2026-04-09T17:24:44.795308+00:00",
            "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
            "event_name": "Demo Event 2024",
            "id": "2eb3ee8a-9774-47cf-8bd7-8500108d011f",
            "is_restricted": true,
            "location_x": 10,
            "location_y": 20,
            "name": "VIP Updated"
        }
    },
    "status": "success"
}
“

12.	When click on a zone can move to a page that list all the companies on the clicked on zone this can be done by calling http://89.167.92.67:3000/api/v1/get_companies_by_zone the method is post and the authorization must be passed, the body as below:
“
{
  "zone_id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
  "page": 1,
  "limit": 20
}
“
The response will be as below:
“
{
    "data": {
        "data": [
            {
                "booth_number": "Z02",
                "created_at": "2026-03-22T12:05:39.927696+00:00",
                "description": null,
                "email": null,
                "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "event_name": "Demo Event 2024",
                "id": "ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2",
                "industry": null,
                "logo_url": "blob:http://localhost:5173/990c24d8-20c6-4e58-9fd3-fc1c70f67cc8",
                "name": "my company1",
                "phone": null,
                "slug": "my-company1",
                "website": null,
                "zone_id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
                "zone_name": "zone11"
            },
            {
                "booth_number": "Z01",
                "created_at": "2026-03-22T12:05:27.967653+00:00",
                "description": null,
                "email": null,
                "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "event_name": "Demo Event 2024",
                "id": "7abd48a5-bcb5-4967-9664-e81389b82672",
                "industry": null,
                "logo_url": null,
                "name": "my company",
                "phone": null,
                "slug": "my-company",
                "website": null,
                "zone_id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
                "zone_name": "zone11"
            },
            {
                "booth_number": "1",
                "created_at": "2026-03-21T20:47:51.422643+00:00",
                "description": "1",
                "email": null,
                "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "event_name": "Demo Event 2024",
                "id": "8eeade0a-8598-44c5-bee7-cc657bd56b13",
                "industry": "1",
                "logo_url": "blob:http://localhost:5173/7557d071-f2ad-44af-81f3-84ce47d6505e",
                "name": "quantom soft",
                "phone": null,
                "slug": "1",
                "website": "1",
                "zone_id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
                "zone_name": "zone11"
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 3
    },
    "status": "success"
}

“
13.	To delete zone http://89.167.92.67:3000/api/v1/delete_zone route must be called the method is post the authorization  must be passed and  the body as below:
“{"id": "7ad4874c-dac5-440f-92a4-b215068f29e7"}”
the response will be as below:
“
{
    "data": {
        "message": "Zone deleted successfully"
    },
    "status": "success"
}
“
14.	when click on companies page must move to companies page and the following route must call http://89.167.92.67:3000/api/v1/retrieve_companies the method is Post and the authorization token must passed, the body as below:
“
{
  "page": 1,
  "limit": 20
}
“
the response as below:
“
{
    "data": {
        "data": [
            {
                "booth_number": "Z02",
                "created_at": "2026-03-22T12:05:39.927696+00:00",
                "description": null,
                "email": null,
                "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "event_name": "Demo Event 2024",
                "id": "ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2",
                "industry": null,
                "logo_url": "blob:http://localhost:5173/990c24d8-20c6-4e58-9fd3-fc1c70f67cc8",
                "name": "my company1",
                "phone": null,
                "slug": "my-company1",
                "website": null,
                "zone_id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
                "zone_name": "zone11"
            },
            {
                "booth_number": "Z01",
                "created_at": "2026-03-22T12:05:27.967653+00:00",
                "description": null,
                "email": null,
                "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "event_name": "Demo Event 2024",
                "id": "7abd48a5-bcb5-4967-9664-e81389b82672",
                "industry": null,
                "logo_url": null,
                "name": "my company",
                "phone": null,
                "slug": "my-company",
                "website": null,
                "zone_id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
                "zone_name": "zone11"
            },
            {
                "booth_number": "1",
                "created_at": "2026-03-21T20:47:51.422643+00:00",
                "description": "1",
                "email": null,
                "event_id": "f882a7ef-ab0d-4363-955d-8f4b39a6d4b2",
                "event_name": "Demo Event 2024",
                "id": "8eeade0a-8598-44c5-bee7-cc657bd56b13",
                "industry": "1",
                "logo_url": "blob:http://localhost:5173/7557d071-f2ad-44af-81f3-84ce47d6505e",
                "name": "quantom soft",
                "phone": null,
                "slug": "1",
                "website": "1",
                "zone_id": "7ad4874c-dac5-440f-92a4-b215068f29e7",
                "zone_name": "zone11"
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 3
    },
    "status": "success"
}
“

15.	to add company the following route must be call the method is post and the authorization must passed http://89.167.92.67:3000/api/v1/add_company the body as below:
“
{
  "zone_id": "2eb3ee8a-9774-47cf-8bd7-8500108d011f",
  "event_id": "295af916-9fbd-4ca4-a98e-2646952b5d8f",
  "name": "New Exhib",
  "booth_number": "B20",
  "slug": "new-exhib",
  "email":"sdfsdfsdfdsf",
  "description":"dsfsdfsfs",
  "industry": "asdasd",
  "website": "sdfsdfs",
  "phone":"sdfsfsf"
}

“
Regarding the zone id and event id must be as a list and they can be retrieved using retrieve_zones and retrieve_events routes. The response of the add_company can be as below:
“
{
    "data": {
        "company": {
            "booth_number": "B20",
            "created_at": "2026-04-09T17:47:09.449948+00:00",
            "description": "dsfsdfsfs",
            "email": "sdfsdfsdfdsf",
            "event_id": "295af916-9fbd-4ca4-a98e-2646952b5d8f",
            "event_name": "فعالية معاذ",
            "id": "16c16615-6990-48b3-895f-7060b0cade2a",
            "industry": "asdasd",
            "logo_url": null,
            "name": "New Exhib",
            "phone": "sdfsfsf",
            "slug": "new-exhib",
            "website": "sdfsdfs",
            "zone_id": "2eb3ee8a-9774-47cf-8bd7-8500108d011f",
            "zone_name": "VIP Updated"
        },
        "message": "Company created successfully"
    },
    "status": "success"
}
“
The email, description, industry, website,  phone are not mandatory.

16.	To update company http://89.167.92.67:3000/api/v1/update_company route will be called, the method is post and authorization must be passed. The body as below:
“
{
"id": "16c16615-6990-48b3-895f-7060b0cade2a",
  "name": "New Exhib",
  "booth_number": "B20",
  "slug": "new-exhib",
  "email":"sdfsdfsdfdsf",
  "description":"dsfsdfsfs",
  "industry": "asdasd",
  "website": "sdfsdfs",
  "phone":"sdfsfsf"
}

“
The response as below:
“
{
    "data": {
        "company": {
            "booth_number": "B20",
            "created_at": "2026-04-09T17:47:09.449948+00:00",
            "description": "dsfsdfsfs",
            "email": "sdfsdfsdfdsf",
            "event_id": "295af916-9fbd-4ca4-a98e-2646952b5d8f",
            "event_name": "فعالية معاذ",
            "id": "16c16615-6990-48b3-895f-7060b0cade2a",
            "industry": "asdasd",
            "logo_url": null,
            "name": "New Exhib",
            "phone": "sdfsfsf",
            "slug": "new-exhib",
            "website": "sdfsdfs",
            "zone_id": "2eb3ee8a-9774-47cf-8bd7-8500108d011f",
            "zone_name": "VIP Updated"
        },
        "message": "Company updated successfully"
    },
    "status": "success"
}
“

17.	To delete company the http://89.167.92.67:3000/api/v1/delete_company must be called, the method is post, the authorization must be passed, the body as below:
“
{
  "id": "16c16615-6990-48b3-895f-7060b0cade2a"
}
“
The response as below:
“
{
    "data": {
        "message": "Company deleted successfully"
    },
    "status": "success"
}
“
18.	when click on the company a page for the company must be open and call http://89.167.92.67:3000/api/v1/retrieve_users with post method and pass the authorization and the following body:

“
{
  "company_id":"ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2"
}

“
The company id which is the id of the company that clicked on. The route will retrieve all the exhibitor_staff under the company, the response as below:
“
{
    "data": {
        "data": [
            {
                "city": "Tripoli",
                "company_id": "ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2",
                "company_name": "my company1",
                "country": "libya",
                "created_at": "2026-03-30T12:29:33.021765+00:00",
                "display_name": "hamza younsu",
                "email": "hamham@gmail.com",
                "first_name": "hamza",
                "id": "816abf15-1b56-41f8-823f-ed4909aadbba",
                "is_active": true,
                "job_title": " exhibitor_staff ",
                "last_name": "younsu",
                "phone": "05343998077",
                "photo_url": " s",
                "roles": [
                    "security"
                ]
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 1
    },
    "status": "success"
}

“
19.	can add a exhibitor_staff under the company by calling http://89.167.92.67:3000/api/v1/add_user the method is post and the authorization must passed, the body as below:
“
{
  "first_name": "moath",
  "last_name": "ali",
  "email": "moathf@a0liz.com",
  "password": "SecurePass123!",
  "phone": "+905343998z0677",
  "job_title": "exhibitor_staff ",
  "country": "USA",
  "company_id":"ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2",
  "city": "NYC"
}
“
The job_title and the company_id will passed to the api from the background there is no need to filled like a textbox.
20.	To update this user which is the exhibitor from inside the company page we can call http://89.167.92.67:3000/api/v1/update_user the method is post and the authorization must passed. The body as below:

“
{
  "id": "b065a62c-e7da-42a9-9e79-bb6ed15babe9",
  "first_name": "moath",
  "last_name": "ali",
  "email": "moathf@a0liz.com",
  "password": "SecurePass123!",
  "phone": "+905343998z0677",
  "country": "USA",
  "city": "NYC"

}
“
The response as below:

“
{
    "data": {
        "message": "User updated successfully",
        "user": {
            "access_token": "2d6bbfbd-ea7b-445e-83ac-84225a236924",
            "auth_id": "None",
            "auth_provider": "email",
            "city": "NYC",
            "company": "<Company(id=ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2, name=my company1, event_id=f882a7ef-ab0d-4363-955d-8f4b39a6d4b2)>",
            "company_id": "ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2",
            "company_name": "my company1",
            "country": "USA",
            "created_at": "2026-04-09 18:05:25.997901+00:00",
            "deleted_at": "None",
            "display_name": "moath ali",
            "email": "moathf@a0liz.com",
            "first_name": "moath",
            "id": "b065a62c-e7da-42a9-9e79-bb6ed15babe9",
            "is_active": "True",
            "is_blacklisted": "False",
            "job_title": "exhibitor_staff ",
            "last_name": "ali",
            "phone": "+905343998z0677",
            "photo_url": "None",
            "roles": [
                {
                    "event_id": null,
                    "name": "exhibitor_staff",
                    "role_id": "e1004725-ea5e-4779-8c37-2a7e0b3071b0"
                }
            ],
            "token_expires_at": "None",
            "token_last_rotated_at": "None",
            "updated_at": "2026-04-09 18:05:25.997901+00:00",
            "user_roles": "[<UserRoles(id=2eaff279-ba85-4a17-b4da-c249f10c8c57, user_id=b065a62c-e7da-42a9-9e79-bb6ed15babe9, role_id=e1004725-ea5e-4779-8c37-2a7e0b3071b0, event_id=None)>]"
        }
    },
    "status": "success"
}
“

21.	to delete use under company the http://89.167.92.67:3000/api/v1/delete_user must be call the method is post and the authorization must be passed, the body as below:
“{ "id": "b065a62c-e7da-42a9-9e79-bb6ed15babe9"}“
the response as below:
“
{
    "data": {
        "message": "User deleted successfully"
    },
    "status": "success"
}
“
22.	when clicking on user page must move to a page and call the following route http://89.167.92.67:3000/api/v1/retrieve_users the method is post and the authorization must be passed. The route will retrieve the whole user types. You must set the user type as fixed list in the frontend. And the user can filter based on the type. The body as below:
“
{
  "page":1,
  "limit":20
}
“
The following body will retrieve all the users as below response:
“
{
    "data": {
        "data": [
            {
                "city": "NYC",
                "company_id": null,
                "company_name": "شركة الاتجاد",
                "country": "USA",
                "created_at": "2026-04-09T16:46:11.021312+00:00",
                "display_name": "moath ali",
                "email": "moathf@a0li.com",
                "first_name": "moath",
                "id": "b91d6e1c-1143-44a3-b0eb-826bde756e12",
                "is_active": true,
                "job_title": "event_admin",
                "last_name": "ali",
                "phone": "+9053439980677",
                "photo_url": null,
                "roles": [
                    "event_admin"
                ]
            },
            {
                "city": "NYC",
                "company_id": null,
                "company_name": "شركة الاتجاد",
                "country": "USA",
                "created_at": "2026-04-09T16:08:40.753540+00:00",
                "display_name": "moath ali",
                "email": "moathf@ali.com",
                "first_name": "moath",
                "id": "39487549-c593-458f-a852-48567ed97a48",
                "is_active": true,
                "job_title": "visitor",
                "last_name": "ali",
                "phone": "+905343998077",
                "photo_url": null,
                "roles": [
                    "visitor"
                ]
            },
            {
                "city": null,
                "company_id": null,
                "company_name": null,
                "country": null,
                "created_at": "2026-04-08T20:50:03.460255+00:00",
                "display_name": "ali ali",
                "email": "ali.atia.k@gmail.com",
                "first_name": "ali",
                "id": "facec047-b95f-4d0f-b3d7-6e5785dc90f5",
                "is_active": true,
                "job_title": "visitor",
                "last_name": "ali",
                "phone": null,
                "photo_url": null,
                "roles": [
                    "visitor"
                ]
            },
            {
                "city": " ",
                "company_id": null,
                "company_name": "شركة تست",
                "country": " ",
                "created_at": "2026-03-31T21:48:31.958486+00:00",
                "display_name": "moaz media",
                "email": "moazmedia22@gmail.com",
                "first_name": "moaz",
                "id": "44b3f540-36ef-44a6-846a-ee31113761b5",
                "is_active": true,
                "job_title": "media",
                "last_name": "media",
                "phone": "55555555",
                "photo_url": " ",
                "roles": [
                    "media"
                ]
            },
            {
                "city": "NYC",
                "company_id": null,
                "company_name": "شركة الاتجاد",
                "country": "USA",
                "created_at": "2026-03-31T21:01:16.608068+00:00",
                "display_name": "John Doe",
                "email": "moathf@aa.com",
                "first_name": "John",
                "id": "65db294f-35b9-4922-80eb-ef37b65a7b9d",
                "is_active": true,
                "job_title": "media",
                "last_name": "Doe",
                "phone": "+12x348fي5s6as78a8440",
                "photo_url": "https://example.com/photo.jpg",
                "roles": [
                    "media"
                ]
            },
            {
                "city": null,
                "company_id": null,
                "company_name": null,
                "country": null,
                "created_at": "2026-03-30T19:57:50.869991+00:00",
                "display_name": "moazevent moazevent",
                "email": "moazevent@gmail.com",
                "first_name": "moazevent",
                "id": "8fbb26a1-396a-4adb-a9be-ab885abdc158",
                "is_active": true,
                "job_title": "event_admin",
                "last_name": "moazevent",
                "phone": null,
                "photo_url": null,
                "roles": [
                    "event_admin"
                ]
            },
            {
                "city": "NYC",
                "company_id": null,
                "company_name": "شركة الاتجاد",
                "country": "USA",
                "created_at": "2026-03-30T13:19:13.135447+00:00",
                "display_name": "John Doe",
                "email": "moathf@cيomxpany.com",
                "first_name": "John",
                "id": "657fd52e-99aa-4bfa-af8d-fcadbc5dcb6e",
                "is_active": true,
                "job_title": "visitor",
                "last_name": "Doe",
                "phone": "+12x348fي56788440",
                "photo_url": "https://example.com/photo.jpg",
                "roles": [
                    "visitor"
                ]
            },
            {
                "city": "NYC",
                "company_id": null,
                "company_name": "شركة الاتجاد",
                "country": "USA",
                "created_at": "2026-03-30T13:14:20.946428+00:00",
                "display_name": "John Doe",
                "email": "moath@cيomxpany.com",
                "first_name": "John",
                "id": "957e60eb-b1dc-4f84-a208-cbeb8f1ca8fc",
                "is_active": true,
                "job_title": "visitor",
                "last_name": "Doe",
                "phone": "+12x348ي56788440",
                "photo_url": "https://example.com/photo.jpg",
                "roles": [
                    "visitor"
                ]
            },
            {
                "city": "Tripoli",
                "company_id": "ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2",
                "company_name": "my company1",
                "country": "libya",
                "created_at": "2026-03-30T12:29:33.021765+00:00",
                "display_name": "hamza younsu",
                "email": "hamham@gmail.com",
                "first_name": "hamza",
                "id": "816abf15-1b56-41f8-823f-ed4909aadbba",
                "is_active": true,
                "job_title": "security",
                "last_name": "younsu",
                "phone": "05343998077",
                "photo_url": " s",
                "roles": [
                    "security"
                ]
            },
            {
                "city": null,
                "company_id": null,
                "company_name": null,
                "country": null,
                "created_at": "2026-03-30T12:22:07.792615+00:00",
                "display_name": "Zakaria Alyafawi",
                "email": "alyafawizakaria@gmail.com",
                "first_name": "Zakaria",
                "id": "d892a48b-b234-42cb-b157-b2646c122bd7",
                "is_active": true,
                "job_title": "visitor",
                "last_name": "Alyafawi",
                "phone": null,
                "photo_url": null,
                "roles": [
                    "visitor"
                ]
            },
            {
                "city": "",
                "company_id": "8eeade0a-8598-44c5-bee7-cc657bd56b13",
                "company_name": "quantom soft",
                "country": "",
                "created_at": "2026-03-28T17:49:05.626955+00:00",
                "display_name": "ziko exhibitor",
                "email": "zikoexhibitor@gmail.com",
                "first_name": "ziko",
                "id": "ac2c704f-311b-439e-9424-65793c9720fd",
                "is_active": true,
                "job_title": "exhibitor_staff",
                "last_name": "exhibitor",
                "phone": null,
                "photo_url": "",
                "roles": [
                    "exhibitor_staff"
                ]
            },
            {
                "city": null,
                "company_id": null,
                "company_name": null,
                "country": null,
                "created_at": "2026-03-28T17:43:29.041830+00:00",
                "display_name": "Ziko visitor",
                "email": "zikovisitor@gmail.com",
                "first_name": "Ziko",
                "id": "6037dac8-f9c3-4850-8cf7-99a7b48e4e64",
                "is_active": true,
                "job_title": "visitor",
                "last_name": "visitor",
                "phone": null,
                "photo_url": null,
                "roles": [
                    "visitor"
                ]
            },
            {
                "city": "Adapazari",
                "company_id": null,
                "company_name": null,
                "country": "Türkiye",
                "created_at": "2026-03-26T14:17:43.671630+00:00",
                "display_name": "moaz23 moaz23",
                "email": "moaz2@gmail.com",
                "first_name": "moaz23",
                "id": "877b1498-4343-418b-a275-8eacd955c97c",
                "is_active": true,
                "job_title": "visitor",
                "last_name": "moaz23",
                "phone": "5555555551",
                "photo_url": "tst",
                "roles": [
                    "visitor"
                ]
            },
            {
                "city": "",
                "company_id": "8eeade0a-8598-44c5-bee7-cc657bd56b13",
                "company_name": "quantom soft",
                "country": "",
                "created_at": "2026-03-26T14:13:36.116819+00:00",
                "display_name": "Moaz Moaz",
                "email": "moazHamaidah@gmail.com",
                "first_name": "Moaz",
                "id": "4ab2f388-5cbb-4846-b8f5-b32a217b659e",
                "is_active": true,
                "job_title": "security",
                "last_name": "Moaz",
                "phone": null,
                "photo_url": "",
                "roles": [
                    "security"
                ]
            },
            {
                "city": "",
                "company_id": "8eeade0a-8598-44c5-bee7-cc657bd56b13",
                "company_name": "quantom soft",
                "country": "",
                "created_at": "2026-03-26T13:19:14.919902+00:00",
                "display_name": "Ziko ZikoTest",
                "email": "zikoTestTestExample@gmail.com",
                "first_name": "Ziko",
                "id": "835b9dbc-023a-4f1e-8e7f-ee0085555b31",
                "is_active": true,
                "job_title": "security",
                "last_name": "ZikoTest",
                "phone": null,
                "photo_url": "",
                "roles": [
                    "security"
                ]
            },
            {
                "city": "NYC",
                "company_id": null,
                "company_name": null,
                "country": "USA",
                "created_at": "2026-03-23T17:14:55.594311+00:00",
                "display_name": "hamza yunsu",
                "email": "hamza11@company.com",
                "first_name": "hamza",
                "id": "524f352b-4639-4587-967f-8eff2ee4f59d",
                "is_active": true,
                "job_title": "exhibitor_staff",
                "last_name": "yunsu",
                "phone": "+12345816bb7890",
                "photo_url": "https://example.com/photo.jpg",
                "roles": []
            },
            {
                "city": "NYC",
                "company_id": null,
                "company_name": null,
                "country": "USA",
                "created_at": "2026-03-16T19:12:55.039586+00:00",
                "display_name": "hamza yunsu",
                "email": "hamza@company.com",
                "first_name": "hamza",
                "id": "7d434cec-c4a0-4afd-8df1-257093029612",
                "is_active": true,
                "job_title": "Staff",
                "last_name": "yunsu",
                "phone": "+12345567891",
                "photo_url": "https://example.com/photo.jpg",
                "roles": []
            },
            {
                "city": null,
                "company_id": null,
                "company_name": null,
                "country": null,
                "created_at": "2026-03-16T15:04:16.618736+00:00",
                "display_name": "Zakaria Alyafawi",
                "email": "zakariaaalyafawi@gmail.com",
                "first_name": "Zakaria",
                "id": "1dc507d3-d390-485e-9fce-b92a77f65496",
                "is_active": true,
                "job_title": null,
                "last_name": "Alyafawi",
                "phone": null,
                "photo_url": null,
                "roles": [
                    "super_admin"
                ]
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 18
    },
    "status": "success"
}
“

To filter based on role the body can be passed as below:

“
{
  "page":1,
  "limit":20,
  "role_name":"media"
}
“

23.	To add user can click on add user, in this page the system admin can add only event_admin, security, and media users, these must be saved in the frontend.  by calling http://89.167.92.67:3000/api/v1/add_user the method is post and the authorization must passed, the body as below:
“
{
  "first_name": "moath",
  "last_name": "ali",
  "email": "moathf@a0lizc.com",
  "password": "SecurePass123!",
  "phone": "+905343998zcc0677",
  "job_title": "media",
  "country": "USA",
  "city": "NYC"
}
“
The job_title will be selected from the sited list in frontend.

24.	To update this usefrom inside the users page we can call http://89.167.92.67:3000/api/v1/update_user the method is post and the authorization must passed. The body as below:

“
{
  "id": "b065a62c-e7da-42a9-9e79-bb6ed15babe9",
  "first_name": "moath",
  "last_name": "ali",
  "email": "moathf@a0liz.com",
  "password": "SecurePass123!",
  "phone": "+905343998z0677",
  "country": "USA",
  "city": "NYC"

}
“
The response as below:

“
{
    "data": {
        "message": "User updated successfully",
        "user": {
            "access_token": "2d6bbfbd-ea7b-445e-83ac-84225a236924",
            "auth_id": "None",
            "auth_provider": "email",
            "city": "NYC",
            "company": "<Company(id=ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2, name=my company1, event_id=f882a7ef-ab0d-4363-955d-8f4b39a6d4b2)>",
            "company_id": "ac9fc53f-3983-4f9e-b73f-cb0c4fdc37f2",
            "company_name": "my company1",
            "country": "USA",
            "created_at": "2026-04-09 18:05:25.997901+00:00",
            "deleted_at": "None",
            "display_name": "moath ali",
            "email": "moathf@a0liz.com",
            "first_name": "moath",
            "id": "b065a62c-e7da-42a9-9e79-bb6ed15babe9",
            "is_active": "True",
            "is_blacklisted": "False",
            "job_title": "media",
            "last_name": "ali",
            "phone": "+905343998z0677",
            "photo_url": "None",
            "roles": [
                {
                    "event_id": null,
                    "name": "media",
                    "role_id": "e1004725-ea5e-4779-8c37-2a7e0b3071b0"
                }
            ],
            "token_expires_at": "None",
            "token_last_rotated_at": "None",
            "updated_at": "2026-04-09 18:05:25.997901+00:00",
            "user_roles": "[<UserRoles(id=2eaff279-ba85-4a17-b4da-c249f10c8c57, user_id=b065a62c-e7da-42a9-9e79-bb6ed15babe9, role_id=e1004725-ea5e-4779-8c37-2a7e0b3071b0, event_id=None)>]"
        }
    },
    "status": "success"
}
“

25.	to delete use under company the http://89.167.92.67:3000/api/v1/delete_user must be call the method is post and the authorization must be passed, the body as below:
“{ "id": "b065a62c-e7da-42a9-9e79-bb6ed15babe9"}“
the response as below:
“
{
    "data": {
        "message": "User deleted successfully"
    },
    "status": "success"
}
“

26.	To logout http://89.167.92.67:3000/api/v1/kill_session route will be called and pass the token in the authorization the method is GET.

The exhibitor_staff, visitor, and media users will login to the platform, the home page will represent there profile and the qr code. Can move to zones and companies page to see the exists companies or zones, this can be done though http://89.167.92.67:3000/api/v1/retrieve_zones and http://89.167.92.67:3000/api/v1/retrieve_companies routes. 

27.	When click on connection page must move to connection page and call http://89.167.92.67:3000/api/v1/retrieve_connections with method post and pass the authorization, the route will retrieve all the connections, the body as below:
“{"page":1, "limit":20}”
the response as below:
“
{
    "data": {
        "data": [
            {
                "company_name": null,
                "display_name": "hamza yunsu",
                "email": "hamza11@company.com",
                "first_name": "hamza",
                "job_title": "exhibitor_staff",
                "last_name": "yunsu",
                "phone": "+12345816bb7890",
                "photo_url": "https://example.com/photo.jpg"
            }
        ],
        "limit": 20,
        "page": 1,
        "total": 1
    },
    "status": "success"
}
“
28.	When click on add connection must open cam to scan qr code. After scanning the qr code must get the access_token from the qr code and request http://89.167.92.67:3000/api/v1/get_user_by_access_token route with post method and pass the authorization, the body will be as below:
“{"access_token": "53f43c21-a098-417a-8766-1a9f84f26f79"}“
The access token which is reeded from the qr code. The response as below:
“
{
    "data": {
        "user": {
            "access_token": "53f43c21-a098-417a-8766-1a9f84f26f79",
            "auth_id": "None",
            "auth_provider": "email",
            "city": "NYC",
            "company": "None",
            "company_id": "None",
            "company_name": null,
            "country": "USA",
            "created_at": "2026-03-23 17:14:55.594311+00:00",
            "deleted_at": "None",
            "display_name": "hamza yunsu",
            "email": "hamza11@company.com",
            "first_name": "hamza",
            "id": "524f352b-4639-4587-967f-8eff2ee4f59d",
            "is_active": "True",
            "is_blacklisted": "False",
            "job_title": "exhibitor_staff",
            "last_name": "yunsu",
            "phone": "+12345816bb7890",
            "photo_url": "https://example.com/photo.jpg",
            "roles": [],
            "token_expires_at": "None",
            "token_last_rotated_at": "None",
            "updated_at": "2026-03-23 17:14:55.594311+00:00",
            "user_roles": "[]"
        }
    },
    "status": "success"
}
“
Which is the user information that will be added will be shown as pop up.
29.	When clicking on add http://89.167.92.67:3000/api/v1/add_connection route will be called the method is post and the authorization must be passed the body as below:
“{"friend_access_token": "53f43c21-a098-417a-8766-1a9f84f26f79"}“
The response as below:
“
{
    "data": {
        "connection": {
            "connected_to_id": "524f352b-4639-4587-967f-8eff2ee4f59d",
            "id": "4742e551-0bba-4451-8b88-d7f3fbc1e0ab",
            "scanned_at": "2026-04-09T18:37:24.091166+00:00"
        },
        "message": "Connection added successfully"
    },
    "status": "success"
}
“

The security stuff will login to the platform, in the home page the security user must select the location where the user will work, can select event or zone can’t select both of them, the selected must be from list, the list of event’s can be come from  http://89.167.92.67:3000/api/v1/retrieve_events route, and the list of zones will come from http://89.167.92.67:3000/api/v1/retrieve_zones. Then the user must select the action enter or exit. The open the camera. For each reading must read the qr code and extract the access token then call http://89.167.92.67:3000/api/v1/scan_validate route, the method is post and the authorization must passed. The body as below:
{"access_token":"a1bb0c75-dbac-4a71-9d05-e211cac410cd", "zone_id":"cd395800-af74-41a4-85b1-9fc64be7eb53", "action":"exit"}
As mentioned before the zone_id or the event_id can be passed, and the action can be enter or exit. And the reeded access token.
Also Can move to zones and companies page to see the exists companies or zones, this can be done though http://89.167.92.67:3000/api/v1/retrieve_zones and http://89.167.92.67:3000/api/v1/retrieve_companies routes.  




Note that:
there is no images for the users so we can take the first char from the user name and set it as image this must handled from the frontend.
Als the platform must support Arabic and English language, also dark and light mode.
The just in the registration section there is no need to pass the authorization where the job title is visitor.
