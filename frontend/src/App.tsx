import { useEffect } from "react";

import { sessionState, useChatSession } from "@chainlit/react-client";
import { Playground } from "./components/playground";
import { Option } from "./components/option";
import { useRecoilValue } from "recoil";

const userEnv = {};

function App() {
  const { connect } = useChatSession();
  const session = useRecoilValue(sessionState);
  useEffect(() => {
    if (session?.socket.connected) {
      return;
    }
    fetch("http://localhost:80/custom-auth")
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        connect({
          userEnv,
          accessToken: `Bearer: ${data.token}`,
        });
      });
  }, [connect]);

  return (
    <div className="flex">
      <div className="w-1/3 bg-[#5f675f] text-white">
        <Option />
      </div>
      <div className="w-2/3">
        <Playground />
      </div>
    </div>
  );
}

export default App;
