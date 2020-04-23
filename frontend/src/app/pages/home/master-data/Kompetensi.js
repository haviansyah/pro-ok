import React, { Component } from 'react';
import getAllJurusan from '../../../crud/jurusan.crud';
import Tbl from '../../../partials/tbl';

export default class Kompetensi extends Component {
    buatColumn(label,filter = false){
        return {
            name: label.toLowerCase(),
            label: label,
            options: {
             filter: filter,
            }
           };
    }
    constructor(props) {
        super(props);
        this.state = { usersCollection: [],
            selesai : false
        };
        const kolom = ["Okupasi","Kode Kompetensi","Kompetensi","Deskripsi","Sikap","Keterampilan","Pengetahuan"];
        this.columns = kolom.map((col, ind) => ind === 0 ? this.buatColumn(col,true) : this.buatColumn(col) )
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

    render() {
        return (
            <div className="col-xl-12">
                {/* <Portlet fluidHeight={true}>
                    <PortletHeader
                    title="Master Data Jurusan"/>

                    <PortletBody> */}
                        
                        { this.state.selesai ?
                            <Tbl title="Master Data Kompetensi" columns={this.columns} data={this.state.usersCollection}></Tbl>
                            : <div></div>
                        }
                    {/* </PortletBody>
                </Portlet> */}
            </div>
        )
    }
}