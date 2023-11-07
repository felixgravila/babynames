import './App.css';
import { ForceGraph2D, ForceGraph3D } from 'react-force-graph';
import SpriteText from 'three-spritetext';

function App() {
  // var data = require("./graph2_358_top3.json")
  var data = require("./graph_545_top0.1.json")

  return <ForceGraph3D
    graphData={data}
    width='100%'
    height='100%'
    nodeThreeObject={node => {
      const sprite = new SpriteText(node.name);
      sprite.color = "yellow";
      sprite.textHeight = 8;
      return sprite;
    }}
  />

}

export default App;
