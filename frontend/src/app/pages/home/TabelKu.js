import React, { Component } from 'react';
import getAllJurusan from '../../crud/jurusan.crud';
import Tbl from '../../partials/tbl';

export default class Users extends Component {

    constructor(props) {
        super(props);
        this.state = { usersCollection: [],
            selesai : false
        };
    }

    componentDidMount() {
        getAllJurusan()
            .then(res => {
                var hasil = []
                res.data.forEach(el => {
                    hasil.push(Object.values(el))
                    
                });
                this.setState({ usersCollection: hasil });
                this.setState({selesai : true})
            })
            .catch(function (error) {
                console.log(error);
            })
    }

    dataTable() {
        return <Tbl data={this.state.usersCollection} header={this.header}></Tbl>
    }

    render() {
        return (
            <div className="col-xl-12">
                {/* <Portlet fluidHeight={true}>
                    <PortletHeader
                    title="Master Data Jurusan"/>

                    <PortletBody> */}
                        
                        { this.state.selesai ?
                            <Tbl data={this.state.usersCollection}></Tbl>
                            : <div></div>
                        }
                    {/* </PortletBody>
                </Portlet> */}
            </div>
        )
    }
}