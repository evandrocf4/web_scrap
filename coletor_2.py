def _parse_table(selector, table_path):
            table_rows = selector.xpath(table_path)
            parsed_table = []
            for index, row in enumerate(table_rows):
                if index == 0:
                    continue
                row_data = {
                    'tipo': row.xpath('.//td[1]//text()').get(''),
                    'data_com': row.xpath('.//td[2]//text()').get(''),
                    'pagamento': row.xpath('.//td[3]//text()').get(''),
                    'valor': row.xpath('.//td[4]//text()').get(''), 
                }
                parsed_table.append(row_data)
        url_statusinvest = 'https://statusinvest.com.br/acoes/vale3'
        self.start_snapshot_engine()
        self.snapshot_engine.get(url_statusinvest)
        self.execute_wait_for_snapshot_engine(xpath='(//table)[1]')
        sleep(1)

        # pra cada página da paginação da tabela
        # 1 - click na página
        # 2 - chama a função que parseia a tabela
        selector = Selector(text=self.snapshot_engine.page_source)

        # pagination_buttons = selector.xpath('//ul[@class="pagination mb-0"]//a[@role="button"]')
        # for index, page in enumerate(pagination_buttons):
        #     if index == 0:
        #         continue
        #     # passa o xpath do button da page
        #     self.snapshot_engine.find_element(By.XPATH, )
        #     selector = Selector(text=self.snapshot_engine.page_source)
        #     parsed_table_section = _parse_table('(//table)[1]//tr')


        # colocar o executable
        table_rows = selector.xpath('(//table)[1]//tr')
        parsed_table = []
        for index, row in enumerate(table_rows):
            if index == 0:
                continue
            row_data = {
                'tipo': row.xpath('.//td[1]//text()').get(''),
                'data_com': row.xpath('.//td[2]//text()').get(''),
                'pagamento': row.xpath('.//td[3]//text()').get(''),
                'valor': row.xpath('.//td[4]//text()').get(''), 
            }
            parsed_table.append(row_data)
                
        print('\n\n\n', parsed_table,'\n\n\n')