import React from "react";
import { Route, Switch } from "react-router-dom";
import Kompetensi from "./Kompetensi";

export default function GoogleMaterialPage() {
    return (
      <Switch>
        {/* Layout */}
        <Route 
          path="/master-data/kompetensi" 
          component={Kompetensi} 
        />
    </Switch>);
}