# Language-Agnostic Port Conflict Resolution

When the user encounters an error indicating that a network port is already in use (e.g., `EADDRINUSE`, `address already in use`), you MUST provide a framework-agnostic command to forcefully terminate the lingering process. 

This happens frequently during development when server processes crash or fail to shut down gracefully, regardless of the technology stack (Node.js, Python, Elixir, Go, etc.).

## The Universal Command
Always suggest the following UNIX command to the user, instructing them to replace `<your_port_number>` with the port number they are trying to free (e.g., 3000, 4000, 8080):

```bash
lsof -ti:<your_port_number> | xargs kill -9
```

**Rule Application:**
1. Do not assume the user knows how to clear a port just because they use a specific framework (e.g. Next.js, Phoenix).
2. Explicitly provide this `lsof` one-liner as a helpful hint whenever an `EADDRINUSE` failure is detected.
3. This is a stack-agnostic troubleshooting step that applies universally across all development environments on macOS/Linux.
