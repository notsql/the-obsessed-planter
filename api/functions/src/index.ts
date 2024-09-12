/**
 * Import function triggers from their respective submodules:
 *
 * import {onCall} from "firebase-functions/v2/https";
 * import {onDocumentWritten} from "firebase-functions/v2/firestore";
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

import { HttpsError, onRequest } from "firebase-functions/v2/https";
// import { onTaskDispatched } from "firebase-functions/v2/tasks";
import * as logger from "firebase-functions/logger";

import { initializeApp } from "firebase-admin/app";
import { getFirestore } from "firebase-admin/firestore";
import { verifySignature } from "@vonage/jwt";

// Start writing functions
// https://firebase.google.com/docs/functions/typescript

interface VonageNCCO {
  action: "record" | "conversation" | "connect" | "talk" | "stream" | "input" | "notify",
  eventUrl?: string[],
}

interface VonageRecordNCCO extends VonageNCCO {
  action: "record",
  format?: "mp3" | "wav",
  beepStart?: boolean,
  transcription?: {
    eventUrl: string[],
    language?: string,
    sentimentAnalysis?: boolean,
  }
}

interface VonageTalkNCCO extends VonageNCCO {
  action: "talk",
  text: string,
  language?: string,
  style?: number,
}

interface VonageInputNCCO extends VonageNCCO {
  action: "input",
  type: Array<"dmtf" | "speech">,
  speech: {
    endOnSilence?: number,
    language?: string,
    context?: string[],
    startTimeout?: number,
    maxDuration?: number,
    saveAudio?: boolean,
    sensitivity?: number,
  }
}


initializeApp();

const db = getFirestore();



export const answer = onRequest({ region: "asia-southeast1" }, async (request, response) => {
  const token = request.headers.authorization?.split(" ")[1] as string;

  if (!verifySignature(token, process.env.VONAGE_API_SECRET as string)) {
    throw new HttpsError("permission-denied", "Invalid token");
  }

  logger.info(request.query);

  const ncco: Array<VonageRecordNCCO | VonageTalkNCCO | VonageInputNCCO> = [
    {
      action: "talk",
      text: "Please leave a message. The 10 seconds recording will start in. 3. 2. 1.",
    },
    // {
    //   action: "record",
    //   beepStart: true,
    //   format: "mp3",
    //   eventUrl: [process.env.RECORDED_URL as string],
    //   transcription: {
    //     eventUrl: [process.env.TRANSCRIBED_URL as string],
    //     language: "en-SG"
    //   }
    // },
    {
      action: "input",
      eventUrl: [process.env.RECORD_URL as string],
      type: ["speech"],
      speech: {
        startTimeout: 3,
        maxDuration: 10,
        saveAudio: true,
        language: "en-SG",
      }
    }
  ]

  response.json(ncco);
});

export const recorded = onRequest({ region: "asia-southeast1" }, async (request, response) => {
  const token = request.headers.authorization?.split(" ")[1] as string;

  if (!verifySignature(token, process.env.VONAGE_API_SECRET as string)) {
    throw new HttpsError("permission-denied", "Invalid token");
  }

  const callId = request.body.conversation_uuid as string;
  const recording_url = request.body.speech.recording_url;
  // const start_time = request.body.start_time;
  // const end_time = request.body.end_time;
  const timestamp = request.body.timestamp;

  logger.info(request.body);

  await db.collection("Callers").doc(callId).set({
    recording_url,
    timestamp
    // start_time,
    // end_time
  });

  response.status(204).send();
});

// export const transcribed = onRequest({ region: "asia-southeast1" }, async (request, response) => {
//   const token = request.headers.authorization?.split(" ")[1] as string;

//   if (!verifySignature(token, process.env.VONAGE_API_SECRET as string)) {
//     throw new HttpsError("permission-denied", "Invalid token");
//   }

//   const callId = request.body.conversation_uuid as string;
//   const transcription_url = request.body.transcription_url;

//   logger.info(request.body);

//   await db.collection("Callers").doc(callId).set({
//     transcription_url,
//   }, { merge: true });

//   response.status(204).send();
// });