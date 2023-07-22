import requests

API_URL = "http://localhost:8000"


def create_new_event():
    event_data = {
        "title": "Python Conference 2023",
        "location": "Laramie",
        "start_date": "2023-03-15 09:00:00",
        "end_date": "2023-03-18 16:00:00",
        "available_tickets": 50,
    }

    response = requests.post(f"{API_URL}/events", json=event_data, timeout=5)

    print(response.json())


def see_all_events():
    response = requests.get(f"{API_URL}/events", timeout=5)
    print(response.json())


def book_ticket():
    ticket_data = {
        "event_id": 1,
        "customer_name": "Jon Doe",
        "customer_email": "test@example.com",
    }

    response = requests.post(f"{API_URL}/tickets", json=ticket_data, timeout=5)

    print(response.json())


def delete_event(event_id: int):
    # Delete an event from the database
    url = f"{API_URL}/events/{event_id}"
    response = requests.delete(url, timeout=5)
    if response.status_code == 200:
        print(f"Event with id {event_id} deleted successfully.")
    else:
        print(f"Error deleting event with id {event_id}: {response.content}")


def main():
    create_new_event()
    create_new_event()
    see_all_events()
    book_ticket()
    delete_event(event_id=2)


if __name__ == "__main__":
    main()
