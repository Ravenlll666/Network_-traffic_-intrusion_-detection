import React, { useState, useEffect } from "react";
const ALERTS = [
  { id:1, level:"CRIT", src:"45.132.88.201",  dst:"10.0.0.15",  type:"Port Scan",     proto:"TCP",  time:"14:32:01", port:"22"  },
  { id:2, level:"CRIT", src:"103.24.56.9",    dst:"10.0.0.3",   type:"Brute Force",   proto:"SSH",  time:"14:31:44", port:"22"  },
  { id:3, level:"CRIT", src:"185.220.101.12", dst:"10.0.0.8",   type:"SQLi Attempt",  proto:"HTTP", time:"14:30:33", port:"80"  },
  { id:4, level:"WARN", src:"192.168.1.104",  dst:"8.8.8.8",    type:"DNS Tunnel",    proto:"UDP",  time:"14:31:22", port:"53"  },
  { id:5, level:"WARN", src:"10.0.0.47",      dst:"10.0.0.1",   type:"ARP Spoof",     proto:"ARP",  time:"14:30:55", port:"—"   },
  { id:6, level:"WARN", src:"5.188.62.140",   dst:"10.0.0.12",  type:"ICMP Flood",    proto:"ICMP", time:"14:29:58", port:"—"   },
  { id:7, level:"WARN", src:"91.108.4.5",     dst:"10.0.0.2",   type:"TOR Exit",      proto:"TCP",  time:"14:29:01", port:"443" },
  { id:8, level:"INFO", src:"10.0.0.23",      dst:"10.0.0.1",   type:"High Bandwidth",proto:"TCP",  time:"14:30:10", port:"443" },
  { id:9, level:"INFO", src:"10.0.0.88",      dst:"45.60.12.100",type:"Unusual Egress",proto:"UDP", time:"14:29:40", port:"8080"},
  {id:10, level:"INFO", src:"192.168.1.202",  dst:"10.0.0.1",   type:"New Device",    proto:"DHCP", time:"14:29:20", port:"67"  },
];

const TOP_SOURCES = [
  { ip:"45.132.88.201",  hits:847, cc:"NL" },
  { ip:"103.24.56.9",    hits:612, cc:"CN" },
  { ip:"185.220.101.12", hits:589, cc:"DE" },
  { ip:"91.108.4.5",     hits:423, cc:"US" },
  { ip:"5.188.62.140",   hits:318, cc:"RU" },
];

const PROTOCOLS = [
  { name:"TCP",   pct:62, color:"#2568C0" },
  { name:"UDP",   pct:24, color:"#1A8A5E" },
  { name:"ICMP",  pct: 9, color:"#C48816" },
  { name:"OTHER", pct: 5, color:"#252B38" },
];

const TRAFFIC = [42,58,39,71,88,63,45,52,94,112,87,76,63,85,143,167,98,76,54,88,121,156,134,98];

const SYSTEM_ROWS = [
  { label:"RULES ACTIVE", val:"1,247", ok:true  },
  { label:"ENGINE",        val:"RUNNING", ok:true  },
  { label:"LAST UPDATE",   val:"2h ago",  ok:true  },
  { label:"MISSED PKTS",   val:"0.01%",   ok:true  },
];

const BG      = "#0C0E12";
const SURF    = "#101318";
const SURF2   = "#0E1016";
const BORDER  = "#191D26";
const BORDF   = "#13161D";
const TEXT    = "#B8C0CC";
const MUTED   = "#3E4655";
const DIM     = "#252B38";
const CRIT    = "#E03E48";
const WARN    = "#C48816";
const INFO    = "#2568C0";
const SAFE    = "#1A8A5E";

const LVL_COLOR = { CRIT, WARN, INFO };
const LVL_BG    = {
  CRIT: "rgba(224,62,72,0.06)",
  WARN: "rgba(196,136,22,0.05)",
  INFO: "rgba(37,104,192,0.05)",
};

const M = { fontFamily:"'JetBrains Mono','Courier New',monospace" };
const S = { fontFamily:"'IBM Plex Sans',system-ui,sans-serif" };

const CSS = `
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500&display=swap');
.nd *{box-sizing:border-box}
.nd-row{
  display:grid;
  grid-template-columns:48px 70px 132px 116px 136px 52px 46px 52px;
  gap:0 6px;align-items:center;
  padding:5px 12px;
  border-bottom:1px solid ${BORDF};
  border-left:2px solid transparent;
  font-family:'JetBrains Mono',monospace;
  font-size:10.5px;cursor:pointer;
  transition:background 0.08s;
}
.nd-row:hover{background:rgba(255,255,255,0.016) !important}
.nd-row.cr{border-left-color:${CRIT}30;background:${LVL_BG.CRIT}}
.nd-row.wn{border-left-color:${WARN}28;background:${LVL_BG.WARN}}
.nd-row.in{border-left-color:${INFO}22;background:${LVL_BG.INFO}}
.nd-fb{
  padding:2px 8px;background:transparent;
  border:1px solid ${BORDER};color:${MUTED};
  font-family:'JetBrains Mono',monospace;
  font-size:9px;letter-spacing:.8px;cursor:pointer;
  transition:all .1s;
}
.nd-fb:hover{color:${TEXT};border-color:${DIM}}
.nd-fb.on{border-color:${INFO};color:${TEXT};background:rgba(37,104,192,.12)}
@keyframes nd-pulse{0%,100%{opacity:1}50%{opacity:.15}}
.nd-pulse{animation:nd-pulse 1.8s ease-in-out infinite}
`;

export default function NIDSDashboard() {
  const [time, setTime] = useState(new Date());
  const [filter, setFilter] = useState("ALL");

  // ML prediction coming from Flask
  const [prediction, setPrediction] = useState(null);
  const [apiError, setApiError] = useState(false);

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  // Get prediction from Flask
  useEffect(() => {
  fetch("http://127.0.0.1:5000/api/predict?row=5")
    .then(response => {
      if (!response.ok) {
        throw new Error("API request failed");
      }
      return response.json();
    })
    .then(data => {
      console.log("ML prediction:", data);
      setPrediction(data);
      setApiError(false);
    })
    .catch(error => {
      console.error("Flask API error:", error);
      setApiError(true);
    });
}, []);
 


  const filtered   = filter === "ALL" ? ALERTS : ALERTS.filter(a => a.level === filter);
  const critCount  = ALERTS.filter(a => a.level === "CRIT").length;
  const warnCount  = ALERTS.filter(a => a.level === "WARN").length;
  const infoCount  = ALERTS.filter(a => a.level === "INFO").length;
  const maxT       = Math.max(...TRAFFIC);

 const STATS = [
  {
    label:"ML PREDICTION",
    val: prediction?.prediction || "LOADING",
    color:
      prediction?.threat_level === "SAFE"
        ? SAFE
        : prediction?.threat_level === "CRITICAL"
        ? CRIT
        : WARN,
    accent:true
  },
  {
    label:"CONFIDENCE",
    val: prediction ? `${prediction.confidence}%` : "--",
    color:INFO,
    accent:false
  },
  {
    label:"THREAT LEVEL",
    val: prediction?.threat_level || "LOADING",
    color:
      prediction?.threat_level === "SAFE"
        ? SAFE
        : prediction?.threat_level === "CRITICAL"
        ? CRIT
        : WARN,
    accent:true
  },
  {
    label:"PROTOCOL",
    val: prediction?.protocol || "--",
    color:MUTED,
    accent:false
  },
  {
    label:"SERVICE",
    val: prediction?.service || "--",
    color:MUTED,
    accent:false
  },
  {
    label:"UPTIME",
    val:"99.9%",
    color:SAFE,
    accent:false
  },
];

  const rowClass = (level) => ({ CRIT:"cr", WARN:"wn", INFO:"in" }[level] || "");

  return (
    <>
      <style>{CSS}</style>
      <div className="nd" style={{ background:BG, color:TEXT, minHeight:"100vh", ...S, fontSize:12 }}>

        {/* ── HEADER ── */}
        <div style={{
          display:"flex", justifyContent:"space-between", alignItems:"center",
          padding:"9px 16px", borderBottom:`1px solid ${BORDER}`, background:SURF2,
        }}>
          <div style={{ display:"flex", alignItems:"center", gap:14 }}>
            <span style={{ ...M, fontSize:12, color:DIM }}>▣</span>
            <span style={{ ...M, fontSize:11, color:MUTED, letterSpacing:1.2 }}>NIDS</span>
            <span style={{ color:"#6A7588", fontSize:11 }}>Network Intrusion Detection System</span>
            <span style={{ ...M, fontSize:9, color:DIM, border:`1px solid ${BORDER}`, padding:"1px 5px" }}>v2.4.1</span>
          </div>
          <div style={{ display:"flex", alignItems:"center", gap:14 }}>
            <span style={{ display:"flex", alignItems:"center", gap:6 }}>
              <span className="nd-pulse" style={{ width:5, height:5, borderRadius:"50%", background:SAFE, display:"inline-block" }} />
              <span
  style={{
    ...M,
    fontSize:9,
    color: apiError ? CRIT : SAFE,
    letterSpacing:1.5
  }}
>
  {apiError ? "API OFFLINE" : "MONITORING"}
</span>
            </span>
            <span style={{ ...M, fontSize:10, color:MUTED }}>
              {time.toLocaleDateString("en-GB", { day:"2-digit", month:"short" })}
            </span>
            <span style={{ ...M, fontSize:10, color:DIM }}>
              {time.toLocaleTimeString("en-GB")}
            </span>
          </div>
        </div>

        <div style={{ padding:"12px 14px", display:"flex", flexDirection:"column", gap:10 }}>

          {/* ── STATS ── */}
          <div style={{ display:"flex", gap:8 }}>
            {STATS.map(s => (
              <div key={s.label} style={{
                flex:1, padding:"10px 13px",
                border:`1px solid ${BORDER}`,
                borderLeft: s.accent ? `2px solid ${s.color}35` : `1px solid ${BORDER}`,
                background: s.accent ? `${s.color}06` : SURF,
              }}>
                <div style={{ ...M, fontSize:9, color:MUTED, letterSpacing:1.2, marginBottom:6 }}>{s.label}</div>
                <div style={{ ...M, fontSize:22, color:s.color, fontWeight:500 }}>{s.val}</div>
              </div>
            ))}
          </div>

          {/* ── MAIN SPLIT ── */}
          <div style={{ display:"flex", gap:10 }}>

            {/* ALERTS TABLE */}
            <div style={{ flex:1, border:`1px solid ${BORDER}`, background:SURF, overflow:"hidden" }}>

              {/* toolbar */}
              <div style={{
                display:"flex", justifyContent:"space-between", alignItems:"center",
                padding:"7px 12px", borderBottom:`1px solid ${BORDER}`, background:SURF2,
              }}>
                <span style={{ ...M, fontSize:9, color:MUTED, letterSpacing:1.8 }}>ALERT FEED</span>
                <div style={{ display:"flex", gap:3 }}>
                  {["ALL","CRIT","WARN","INFO"].map(f => (
                    <button key={f} className={`nd-fb${filter===f?" on":""}`} onClick={() => setFilter(f)}>{f}</button>
                  ))}
                </div>
              </div>

              {/* column heads */}
              <div style={{
                display:"grid",
                gridTemplateColumns:"48px 70px 132px 116px 136px 52px 46px 52px",
                gap:"0 6px", padding:"4px 12px",
                borderBottom:`1px solid ${BORDER}`, background:BG,
              }}>
                {["LEVEL","TIME","SOURCE","DEST","TYPE","PROTO","PORT",""].map((h,i) => (
                  <span key={i} style={{ ...M, fontSize:9, color:DIM, letterSpacing:.8 }}>{h}</span>
                ))}
              </div>

              {/* rows */}
              {filtered.map(a => (
                <div key={a.id} className={`nd-row ${rowClass(a.level)}`}>
                  <span style={{
                    display:"inline-block", padding:"1px 4px", fontSize:9,
                    color:LVL_COLOR[a.level],
                    border:`1px solid ${LVL_COLOR[a.level]}30`,
                    background:`${LVL_COLOR[a.level]}09`,
                    letterSpacing:.4,
                  }}>{a.level}</span>
                  <span style={{ color:MUTED }}>{a.time}</span>
                  <span style={{ color:"#92A0B2" }}>{a.src}</span>
                  <span style={{ color:MUTED }}>{a.dst}</span>
                  <span style={{ color:TEXT }}>{a.type}</span>
                  <span style={{ color:MUTED }}>{a.proto}</span>
                  <span style={{ color:DIM }}>{a.port}</span>
                  <span style={{
                    fontSize:9, letterSpacing:.5, cursor:"pointer",
                    color: a.level==="CRIT" ? CRIT : DIM,
                    textDecoration: a.level==="CRIT" ? "underline" : "none",
                  }}>
                    {a.level==="CRIT" ? "BLOCK" : a.level==="WARN" ? "FLAG" : "LOG"}
                  </span>
                </div>
              ))}
            </div>

            {/* SIDEBAR */}
            <div style={{ width:210, display:"flex", flexDirection:"column", gap:8 }}>

              {/* Top sources */}
              <div style={{ border:`1px solid ${BORDER}`, background:SURF, padding:"10px 12px" }}>
                <div style={{ ...M, fontSize:9, color:MUTED, letterSpacing:1.8, marginBottom:10 }}>TOP ATTACK SOURCES</div>
                {TOP_SOURCES.map((s, i) => (
                  <div key={i} style={{
                    display:"flex", justifyContent:"space-between", alignItems:"center",
                    padding:"5px 0",
                    borderBottom: i < TOP_SOURCES.length-1 ? `1px solid ${BORDF}` : "none",
                  }}>
                    <div>
                      <div style={{ ...M, fontSize:10, color:"#7E8E9E" }}>{s.ip}</div>
                      <div style={{ ...M, fontSize:9, color:DIM }}>AS · {s.cc}</div>
                    </div>
                    <span style={{ ...M, fontSize:10, color: i < 2 ? CRIT : WARN }}>{s.hits}</span>
                  </div>
                ))}
              </div>

              {/* Protocol split */}
              <div style={{ border:`1px solid ${BORDER}`, background:SURF, padding:"10px 12px" }}>
                <div style={{ ...M, fontSize:9, color:MUTED, letterSpacing:1.8, marginBottom:10 }}>PROTOCOL SPLIT</div>
                {PROTOCOLS.map((p, i) => (
                  <div key={i} style={{ marginBottom:9 }}>
                    <div style={{ display:"flex", justifyContent:"space-between", marginBottom:4 }}>
                      <span style={{ ...M, fontSize:9, color:"#5A6578" }}>{p.name}</span>
                      <span style={{ ...M, fontSize:9, color:DIM }}>{p.pct}%</span>
                    </div>
                    <div style={{ background:BORDF, height:2 }}>
                      <div style={{ width:`${p.pct}%`, height:"100%", background:p.color }} />
                    </div>
                  </div>
                ))}
              </div>

              {/* System status */}
              <div style={{ border:`1px solid ${BORDER}`, background:SURF, padding:"10px 12px" }}>
                <div style={{ ...M, fontSize:9, color:MUTED, letterSpacing:1.8, marginBottom:10 }}>SYSTEM STATUS</div>
                {SYSTEM_ROWS.map((r, i) => (
                  <div key={i} style={{
                    display:"flex", justifyContent:"space-between",
                    padding:"4px 0",
                    borderBottom: i < SYSTEM_ROWS.length-1 ? `1px solid ${BORDF}` : "none",
                  }}>
                    <span style={{ ...M, fontSize:9, color:DIM }}>{r.label}</span>
                    <span style={{ ...M, fontSize:9, color: r.ok ? SAFE : CRIT }}>{r.val}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* ── TRAFFIC CHART ── */}
          <div style={{ border:`1px solid ${BORDER}`, background:SURF, padding:"9px 12px" }}>
            <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:8 }}>
              <span style={{ ...M, fontSize:9, color:MUTED, letterSpacing:1.8 }}>PACKET VOLUME · LAST 24H</span>
              <div style={{ display:"flex", gap:14 }}>
                {[["#2568C0","NORMAL"],["#E03E48","SPIKE"]].map(([c,l]) => (
                  <span key={l} style={{ ...M, fontSize:9, color:DIM }}>
                    <span style={{ color:c }}>■</span> {l}
                  </span>
                ))}
              </div>
            </div>
            <svg width="100%" height="52" viewBox="0 0 960 52" preserveAspectRatio="none" style={{ display:"block" }}>
              {TRAFFIC.map((v, i) => {
                const bh = Math.max(2, Math.round((v / maxT) * 44));
                const bw = 960 / TRAFFIC.length;
                return (
                  <rect key={i}
                    x={i * bw + 1} y={52 - bh}
                    width={Math.max(1, bw - 2)} height={bh}
                    fill={v > 115 ? "rgba(224,62,72,.52)" : "rgba(37,104,192,.35)"}
                  />
                );
              })}
            </svg>
            <div style={{ display:"flex", justifyContent:"space-between", marginTop:4, ...M, fontSize:8, color:DIM }}>
              {["00:00","04:00","08:00","12:00","16:00","20:00","now"].map(t => (
                <span key={t}>{t}</span>
              ))}
            </div>
          </div>

        </div>
      </div>
    </>
  );
}
