import React from 'react';
import { Pie, Bar, Line} from 'react-chartjs-2';
import { VisualCard, VisualContainer, VisualH1, VisualWrapper } from './ChartElements';


const BarChart = () => {    
    return (
        <VisualContainer id ='donations'>
            <VisualH1>Know About Us</VisualH1>
            <VisualWrapper>
                <VisualCard>
                <Pie color="#70CAD1" data={{
                labels: ['Books', 'Stationary', 'Sponsorship', 'Study materials', 'Membership', 'Equipments'],
                datasets: [{
                    label: 'products', data: [12, 19, 3, 5, 2, 3], backgroundColor: ['rgba(255,99,132,0.2)', 'rgba(54,162,235,0.2)', 'rgba(255,206,86,0.2)', 'rgba(75,192,192,0.2)', 'rgba(153,102,255,0.2)', 'rgba(255,159,64,0.2)'], borderColor: ['rgba(255,99,132,1)', 'rgba(54,162,235,1)', 'rgba(255,206,86,1)', 'rgba(75,192,192,1)', 'rgba(153,102,255,1)', 'rgba(255,159,64,1)'],
                    borderWidth: 1,
                },
                ]
            }}
                height={300} width={100}
                options={{
                    maintainAspectRatio: false,
                    scales: {
                        yAxes: [{
                            scaleLabel: {
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true,
                            },
                            gridLines: {
                                drawOnChartArea: false
                            }
                        }],
                    },
                
                }
                } />
                </VisualCard>
                <VisualCard>
                <Line color="#70CAD1" data={{
                labels: ['Matlab', 'Serverless', 'Python', 'Data structures', 'Psychology', 'Web development'],
                datasets: [{
                    label: 'Workshops', data: [12, 19, 3, 5, 2, 3], backgroundColor: ['rgba(255,99,132,0.2)', 'rgba(54,162,235,0.2)', 'rgba(255,206,86,0.2)', 'rgba(75,192,192,0.2)', 'rgba(153,102,255,0.2)', 'rgba(255,159,64,0.2)'], borderColor: ['rgba(255,99,132,1)', 'rgba(54,162,235,1)', 'rgba(255,206,86,1)', 'rgba(75,192,192,1)', 'rgba(153,102,255,1)', 'rgba(255,159,64,1)'],
                    borderWidth: 1,
                },
                ]
            }}
                height={300} width={100}
                options={{
                    maintainAspectRatio: false,
                }
                } />
                </VisualCard>
                <VisualCard>
                <Bar color="#70CAD1" data={{
                labels: ['Teachers', 'Students', 'Membership', 'Sponsors', 'Volunteers', 'Equipment Donors'],
                datasets: [{
                    label: 'Users', data: [83, 92, 70, 60, 65, 73], backgroundColor: ['rgba(255,99,132,0.2)', 'rgba(54,162,235,0.2)', 'rgba(255,206,86,0.2)', 'rgba(255,159,64,1)', 'rgba(153,102,255,0.2)', 'rgba(255,159,64,0.2)'], borderColor: ['rgba(255,99,132,1)', 'rgba(54,162,235,1)', 'rgba(255,206,86,1)', 'rgba(255,159,64,1)', 'rgba(153,102,255,1)', 'rgba(255,159,64,1)'],
                    borderWidth: 1,
                },
                ]
            }}
                height={300} width={100}
                options={{
                    maintainAspectRatio: false,
                }
                } />
                </VisualCard>
                </VisualWrapper>
        </VisualContainer>
    )
}

export default BarChart;