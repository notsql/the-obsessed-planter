import { Hono } from 'hono'

const app = new Hono<{ Bindings: CloudflareBindings }>()

app.get("/webhooks/answer", ({ env, req, json }) => {
  const caller = req.query("from");

  console.log(caller)

  return json([
    {
      action: "talk",
      text: "Hello! Please leave a message after the beep."
    },
    {
      action: "record",
      format: "mp3",
      beepStart: true,
      eventUrl: [`${env.API_HOST}/webhooks/recordings`]
    }
  ])
})

app.post("/webhooks/recordings", ({ body, text }) => {
  const recordingUrl = body("recording_url");

  console.log(recordingUrl)

  return text("", 204)
});

export default app;