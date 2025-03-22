from vector_etl import create_flow

flow = create_flow()
flow.load_yaml('./config.yaml')
flow.execute()