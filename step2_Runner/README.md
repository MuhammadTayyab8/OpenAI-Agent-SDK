# Stream Events

### 🔹 1. `AgentUpdatedStreamEvent`

yeh tab aata hai jab agent **start hota hai** ya uski config update hoti hai.
👉 basically "Math Agent" ban gaya, uske tools attach ho gaye (`add_number`), aur lifecycle officially start hua.

---

### 🔹 2. `RawResponsesStreamEvent (response.created)`

LLM (gemini-2.0-flash) ne ek **naya response object create** kiya.
👉 iska matlab: model ready hai instructions process karne ke liye. Abhi koi output nahi bheja, bas ek empty response object bana.

---

### 🔹 3. `RawResponsesStreamEvent (response.output_item.added)`

model ne decide kiya: "Mujhe ek tool call karna hai".
👉 isne ek `ResponseFunctionToolCall` item banaya, jisme `arguments={"a":3,"b":5}` aur `name="add_number"`.

---

### 🔹 4. `RawResponsesStreamEvent (response.function_call_arguments.delta)`

yeh ek **streaming delta** event hai.
👉 matlab model arguments ko ek hi chunk me bhej raha hai (`{"b":5,"a":3}`).
Agar arguments bade hote, toh multiple deltas me aate.

---

### 🔹 5. `RawResponsesStreamEvent (response.output_item.done)`

tool call ka **ek output item close** kar diya.
👉 is point pe model keh raha hai: "haan, maine poore arguments bhej diye, ab done hai".

---

### 🔹 6. `RawResponsesStreamEvent (response.completed)`

response object ka state **complete** mark ho gaya.
👉 abhi tak sirf tool call issue hua hai, koi final text answer nahi.

---

### 🔹 7. `RunItemStreamEvent (tool_called)`

Runner side se event aya: "Tool call request aayi hai".
👉 yaha tum dekh sakte ho ki `add_number` ko call karne ka instruction ready hai, arguments ke sath.

---

### 🔹 8. `RunItemStreamEvent (tool_output)`

tool run hua, aur output aaya → `11`.
👉 ab agent ke paas actual result hai jo woh final output banayega.

---

✅ Finally, `Final Output: 11` print hua.

---

### 🔗 Connection

socha jae to flow kuch aisa hai:

1. **Agent setup** → `AgentUpdatedStreamEvent`
2. **Model start response** → `response.created`
3. **Model ne tool call decide kiya** → `response.output_item.added + delta + done`
4. **Response complete** → `response.completed`
5. **Runner executed tool** → `tool_called` → `tool_output`
6. **Final Output mil gaya**

---
