# Phoenix LiveView Development: Core Knowledge Base (v1.8+)

## 1. Architectural Philosophy: The CRC Pattern
The guiding principle for all Elixir and LiveView logic is Construct, Reduce, Convert (CRC).

* **Construct:** Create a data structure of a core type from convenient inputs (e.g., initializing a socket in mount/3).
* **Reduce:** Transform a term of the core type into another term of that same type through single-purpose functions.
* **Convert:** Transform the final core type into a different type or representation (e.g., render/1 converting socket state to HEEx markup).

## 2. Layered Code Organization
Organize code into three distinct layers to ensure maintainability:

| Layer | Responsibility | Location | Tools |
| :--- | :--- | :--- | :--- |
| **Core** | Pure logic, predictable functions, and schemas. | lib/app/domain/ | Pipelines (|>) |
| **Boundary** | Context APIs, side effects (DB/APIs), and uncertainty. | lib/app/domain.ex | with statements |
| **Presentation**| UI logic, event handling, and real-time updates. | lib/app_web/live/ | LiveView/Components |

## 3. Phoenix 1.8+ & LiveView 1.0/1.1 Key Features

### A. Dedicated Form Pages
* **Abolish Modals:** Phoenix 1.8 replaces complex modal-based CRUD with dedicated pages to improve accessibility and simplify state.
* **Dedicated Form LiveView:** Use a standalone LiveView module (e.g., ProductLive.Form) to handle both :new and :edit actions.
* **Routing Pattern:** Define routes for specific actions mapping to the same form module: live "/products/new", ProductLive.Form, :new.

### B. User Scopes System
* **Secure by Default:** Use the Scope struct to wrap user context and authorization data throughout the request life cycle.
* **Automatic Propagation:** The on_mount callback automatically transfers the scope from the connection to the LiveView socket.
* **Context API Integration:** Business logic functions should accept %Scope{} as the first parameter to ensure data isolation.

### C. LiveView Streams
* **Memory Efficiency:** Use stream/4 for large collections to avoid keeping full lists in server-side memory.
* **DOM Updates:** Use stream_insert/3 and stream_delete/3 to manage UI updates directly in the client-side DOM.

### D. HEEx & Interpolation
* **Embedded Rendering:** Prefer defining the render/1 function directly in the LiveView module using the ~H sigil.
* **Curly Braces:** Use {} for attribute values and interpolations (e.g., id={@id} or {@message}) instead of traditional <%= %>.

## 4. Component Strategy
* **Function Components:** Use for stateless, reusable markup and styling (e.g., .header, .table). Declare APIs using the attr and slot macros.
* **Live Components:** Use when a UI section requires its own interactive state and local event handlers.
* **Targeting:** Always use phx-target={@myself} in Live Components to ensure events are handled by the component rather than the parent view.

## 5. Real-Time & Distributed Features
* **PubSub:** Use Phoenix.PubSub to synchronize state across different processes or users (e.g., updating a dashboard when another user completes a survey).
* **Presence:** Use Phoenix.Presence to track active user activity or site engagement in real time.
* **JS Interop:** Use Phoenix.LiveView.JS commands (e.g., JS.toggle, JS.push) for client-side interactions to avoid unnecessary server round-trips.

## 6. Testing Strategy
* **Unit Tests:** Test reducer functions in isolation using ExUnit. Use "Assertion Reducers" (e.g., |> assert_keys(:score, 0)) to maintain clean pipelines.
* **Integration Tests:** Use Phoenix.LiveViewTest functions:
    * live/2 to spawn the view.
    * element/3 and render_change/2 to simulate interactions.
    * send(view.pid, message) to test PubSub and distributed updates.
* **Zero JS Requirement:** Test all LiveView logic in pure Elixir without relying on external JavaScript testing frameworks.