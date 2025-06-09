Event Booking (MVP)

Business Case:
A mini-system for online event booking and management.
Users can:
1. Submit an event request (order)
2. Register for a limited special promo code
3. Track the real-time progress of promo requests on the site

All orders are saved in the database for further processing by managers.


Business requirements:
1. Allow clients to quickly request event planning services online at any time without visiting the office or calling.
2. Provide a clear, reassuring confirmation that their request was received and will be processed.
3. Offer a limited-time special promotion to encourage users to try the new service (promo code for the first 10 sign-ups).
4. Allow clients to see, in real time, how their promotional request is being handled, increasing trust and transparency.
5. Allow the business team to review all submitted requests for quick response and analytics easily.


Architecture: 
- Frontend: HTML + JavaScript, simple site with an order form and promo code registration. Real-time status updates via WebSocket.
- Backend: Flask (Python), REST API for orders, WebSocket server for streaming status, integrated with a message queue.
- Queue: RabbitMQ for asynchronous processing of email subscriptions (decouples request and processing).
- Consumer: Separate Python service; pulls emails from the queue, simulates processing, streams status updates to the website.
- Database: SQLite — stores all event requests (on-premises, lightweight for MVP).
 

Explanation of architecture choice: 
1. Backend (Flask API + WebSocket):
Receives requests from the website, stores orders in the database, pushes emails into the queue, and streams processing updates to users in real time.
2. RabbitMQ (Queue):
Acts as a buffer, ensuring all promo code requests are processed in strict order and can handle sudden spikes in user activity without losing data.
3. Notifier Service (Consumer):
Continuously listens to the queue, processes each promo request, and communicates status updates back to the backend for real-time user feedback.
4. SQLite Database:
Securely stores all event orders for management review, analytics, and follow-up.

