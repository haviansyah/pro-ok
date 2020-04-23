import React, { Component } from 'react'
import MUIDataTable from "mui-datatables";

export default class Tbl extends Component {
   
    constructor(props){
        super(props);
        

        this.options = {
        filterType: 'checkbox',
        // selectableRowsHeader : false,
        // selectableRows : 'none'
        };
    }
    render() {
        return <MUIDataTable
        title={this.props.title}
        data={this.props.data}
        columns={this.props.columns}
        options={this.options}
      />
    }

}