import React from 'react';
import './App.css';
import { ForceGraph3D } from 'react-force-graph';
import SpriteText from 'three-spritetext';
import Form from 'react-bootstrap/Form'

function App() {

  const datasources = [
    ["Girls top 545 10% links", require("./graph_F_545_top0.1.json")],
    ["Girls top 1346 10% links", require("./graph_F_1346_top0.1.json")],
    ["Girls top 1346 5% links", require("./graph_F_1346_top0.05.json")],
    ["Boys top 475 10% links", require("./graph_M_475_top0.1.json")],
    ["Boys top 963 10% links", require("./graph_M_963_top0.1.json")],
    ["Boys top 963 5% links", require("./graph_M_963_top0.05.json")],
  ]

  const loaded_datasources = {}

  const [linkVis, setLinkVis] = React.useState(false);
  const [pointerInteraction, setPointerInteraction] = React.useState(true);
  const [data, setData] = React.useState(datasources[0][1])


  function toggleLinkVis() {
    setLinkVis(!linkVis)
  }
  function togglePointerInteraction() {
    setPointerInteraction(!pointerInteraction)
  }

  function dropdownChanged(e) {
    setData(datasources[e.target.value][1])
  }


  return <div id="bigdiv">
    <div id="graphdiv">
      <ForceGraph3D
        graphData={data}
        width={window.innerWidth - 200}
        height="100%"
        linkVisibility={linkVis}
        linkResolution={1}
        linkOpacity={0.05}
        warmupTicks={10}
        cooldownTime={20000}
        enablePointerInteraction={pointerInteraction}
        enableNodeDrag={false}
        nodeThreeObject={node => {
          const sprite = new SpriteText(node.name);
          sprite.color = "yellow";
          sprite.textHeight = 8;
          return sprite;
        }}
      />
    </div>
    <div id="selectdiv">
      <div>
        <Checkbox
          label="Show links"
          value={linkVis}
          onChange={toggleLinkVis}
        />
        <Checkbox
          label="Pointer interaction"
          value={pointerInteraction}
          onChange={togglePointerInteraction}
        />
      </div><div>
        <Form.Select aria-label="Default select example" onChange={dropdownChanged}>
          {
            datasources.map((d, idx) => {
              return <option value={idx}>{d[0]}</option>
            })
          }
        </Form.Select>
      </div>
    </div>
  </div>
}

const Checkbox = ({ label, value, onChange }) => {
  return (
    <label>
      <input type="checkbox" checked={value} onChange={onChange} />
      {label}
    </label>
  );
};

export default App;
