import { useEffect, useMemo, useRef, useState } from "react";
import { Activity, Cpu, Radio, ShieldCheck, Wifi, Zap } from "lucide-react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
const WS = API.replace(/^http/, "ws");

const initial = {
  status: "connecting",
  presence: { count: 0, confidence: 0 },
  activity: "idle",
  signal: { strength: 0.5, rssi_dbm: -70, channel: 6, bandwidth_mhz: 20 },
  devices: [],
  alerts: [],
};

function useJarvis() {
  const [state, setState] = useState(initial);
  const [events, setEvents] = useState([]);
  const [connected, setConnected] = useState(false);
  const lastSequence = useRef(0);
  const reconnect = useRef(0);

  useEffect(() => {
    let socket;
    let cancelled = false;
    let timer;

    fetch(API + "/api/v1/state")
      .then((response) => response.json())
      .then((data) => { if (!cancelled) setState(data); })
      .catch(() => {});

    const connect = () => {
      if (cancelled) return;
      socket = new WebSocket(WS + "/ws");

      socket.onopen = () => {
        reconnect.current = 0;
        setConnected(true);
        setState((current) => ({ ...current, status: "online" }));
      };

      socket.onmessage = (message) => {
        const event = JSON.parse(message.data);
        if (event.sequence && event.sequence < lastSequence.current) return;
        lastSequence.current = event.sequence || lastSequence.current;

        setEvents((items) => [event, ...items].slice(0, 12));
        setState((current) => {
          const payload = event.payload || {};
          if (event.event === "human.detected") {
            return { ...current, presence: { count: payload.count, confidence: payload.confidence } };
          }
          if (event.event === "human.lost") {
            return { ...current, presence: { count: 0, confidence: payload.confidence } };
          }
          if (event.event === "activity.changed") {
            return { ...current, activity: payload.activity };
          }
          if (event.event === "signal.updated") {
            return { ...current, signal: { ...current.signal, ...payload } };
          }
          return current;
        });
      };

      socket.onclose = () => {
        setConnected(false);
        setState((current) => ({ ...current, status: "reconnecting" }));
        const delay = Math.min(30000, 1000 * Math.pow(2, reconnect.current++));
        timer = setTimeout(connect, delay);
      };

      socket.onerror = () => socket.close();
    };

    connect();

    return () => {
      cancelled = true;
      clearTimeout(timer);
      socket?.close();
    };
  }, []);

  return { state, events, connected };
}

function Core({ state }) {
  const active = state.presence.count > 0;
  const activity = state.activity;
  const speed = activity === "walking" ? "fast" : activity === "running" ? "faster" : "normal";

  return (
    <section className={"core-panel " + (active ? "is-active " : "") + "activity-" + speed}>
      <div className="core-grid" />
      <div className="core-ring ring-one" />
      <div className="core-ring ring-two" />
      <div className="core-ring ring-three" />
      <div className="scan-line" />
      <div className="core-center">
        <div className="core-mark"><Zap size={22} /></div>
        <strong>{active ? "HUMAN DETECTED" : "SENSING"}</strong>
        <span>{Math.round(state.presence.confidence * 100)}% CONFIDENCE</span>
      </div>
      <div className="core-caption">
        <span>JARVIS CORE</span>
        <span>ACTIVITY / {activity.toUpperCase()}</span>
      </div>
    </section>
  );
}

function Waveform({ strength }) {
  const bars = useMemo(() => Array.from({ length: 42 }, (_, index) => {
    const wave = Math.sin(index * 0.72) * 0.3 + Math.sin(index * 0.19) * 0.2 + strength * 0.45;
    return Math.max(10, Math.min(88, 30 + wave * 70));
  }), [strength]);

  return (
    <div className="waveform">
      {bars.map((height, index) => <i key={index} style={{ height: height + "%" }} />)}
    </div>
  );
}

export default function App() {
  const { state, events, connected } = useJarvis();
  const confidence = Math.round(state.presence.confidence * 100);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-orb" />
          <div><span>JARVIS</span><small>WIFI HUMAN DETECTION</small></div>
        </div>
        <div className="status">
          <span className={"status-dot " + (connected ? "online" : "offline")} />
          {state.status.toUpperCase()}
          <span className="sequence">SEQ {events[0]?.sequence ?? 0}</span>
        </div>
      </header>

      <div className="layout">
        <aside className="rail left-rail">
          <div className="eyebrow"><Radio size={14} /> SENSOR ARRAY</div>
          {state.devices.map((device) => (
            <div className="device-card" key={device.id}>
              <div className="device-title"><span>{device.id}</span><span className="mini-dot" /></div>
              <strong>{device.name}</strong>
              <small>{device.zone} · {Math.round(device.signal_strength * 100)}% link</small>
            </div>
          ))}
          <div className="metric-card">
            <small>PRESENCE</small>
            <strong>{state.presence.count}</strong>
            <span>{confidence}% confidence</span>
          </div>
        </aside>

        <div className="center">
          <Core state={state} />
          <div className="telemetry-row">
            <div><small>CHANNEL</small><strong>{state.signal.channel}</strong></div>
            <div><small>BANDWIDTH</small><strong>{state.signal.bandwidth_mhz} MHz</strong></div>
            <div><small>RSSI</small><strong>{Math.round(state.signal.rssi_dbm)} dBm</strong></div>
            <div><small>ACTIVITY</small><strong>{state.activity}</strong></div>
          </div>
        </div>

        <aside className="rail right-rail">
          <div className="panel">
            <div className="panel-head"><span><Activity size={14} /> CSI SIGNAL</span><b>{Math.round(state.signal.strength * 100)}%</b></div>
            <Waveform strength={state.signal.strength} />
            <div className="signal-foot"><span>LIVE STREAM</span><span>{Math.round(state.signal.rssi_dbm)} dBm</span></div>
          </div>

          <div className="panel">
            <div className="panel-head"><span><Cpu size={14} /> ACTIVITY LOG</span><span>LIVE</span></div>
            <div className="event-list">
              {events.slice(0, 7).map((event) => (
                <div className="event" key={event.event_id}>
                  <span className="event-time">{event.timestamp ? new Date(event.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "--:--:--"}</span>
                  <strong>{event.event.replace(".", " / ")}</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="panel health">
            <div className="panel-head"><span><ShieldCheck size={14} /> SYSTEM HEALTH</span><span className="healthy">NOMINAL</span></div>
            <div className="health-line"><span>REALTIME LINK</span><b>{connected ? "STABLE" : "RECONNECTING"}</b></div>
            <div className="health-line"><span>CSI STREAM</span><b>ACTIVE</b></div>
            <div className="health-line"><span>MODEL</span><b>SIMULATOR</b></div>
          </div>
        </aside>
      </div>

      <footer className="footer">
        <span><Wifi size={13} /> CAMERA-FREE SENSING</span>
        <span>PRIVACY-FIRST · EVENT CONTRACT v1</span>
      </footer>
    </main>
  );
}
