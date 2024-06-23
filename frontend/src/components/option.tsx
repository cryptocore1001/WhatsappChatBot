import { useState } from "react";

const weeks: string[] = [
  "Week 1",
  "Week 2",
  "Week 3",
  "Week 4",
  "Week 5",
  "Week 6",
  "Week 7",
  "Week 8",
  "Week 9",
  "Week 10",
  "Week 11",
  "Week 12",
];
export function Option() {
    const [assistantType, setAssistantType] = useState("");
    const [selectedWeek, setSelectedWeek] = useState("Week 1");
    const [isSelectedJustChat, setIsSelectedJustChat] = useState(false);
    const [isSelectedPGAssistant, setIsSelectedPGAssistant] = useState(false);
    const pgAssistant = () => {
      setAssistantType("program-assistant");
      setIsSelectedJustChat(false);
      setIsSelectedPGAssistant(true);
    }
    const justChat = () => {
      setAssistantType("just-chat");
      setIsSelectedJustChat(true);
      setIsSelectedPGAssistant(false);
    }
  return (
    <div>
      <div className="m-1 border rounded-lg border-slate-700 ">
        <h2 className={`text-xl text-start md:text-2xl font-bold p-4 hover:bg-[#494e49] cursor-pointer ${selectedWeek === "Week 1" && 'bg-[#494e49]'} ${isSelectedJustChat ? 'bg-[#494e49]' : ''}`} onClick={justChat}>
          Just Chat
        </h2>
        <hr className="border-slate-700" />
        <div className="flex flex-col">
            <p className="p-2 text-lg">Please select a week</p>
          {weeks.map((week) => (
            <div key={week} className="flex ml-20 md:ml-40 p-2 text-lg">
              <input
                type="radio"
                id={week}
                name="week"
                value={week}
                className="mr-2 cursor-pointer"
                checked={week === selectedWeek}
                onClick={() => {
                    justChat();
                    setSelectedWeek(week)
                }}
              />
              <label htmlFor={week}>{week}</label>
            </div>
          ))}
        </div>
      </div>
      <div className={`m-1 text-start border rounded-lg border-slate-700 hover:bg-[#494e49] cursor-pointer ${isSelectedPGAssistant ? 'bg-[#494e49]' : ''}`} onClick={pgAssistant}>
          <p className="text-start text-lg md:text-2xl font-bold p-4"> Program Assistant</p>
      </div>
    </div>
  );
}
