import React, { Component } from 'react';

class DataTable extends Component {
    render() {
        return (
            <tr>
                <td>
                    {this.props.obj.kode_jurusan}
                </td>
                <td>
                    {this.props.obj.nama_jurusan}
                </td>
            </tr>
        );
    }
}

export default DataTable;