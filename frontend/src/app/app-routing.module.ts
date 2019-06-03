import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AutoSearchComponent } from './auto-search/auto-search.component';
import { SearchFilterComponent } from './search-filter/search-filter.component';


const routes: Routes = [
  { path: '', redirectTo: '/search', pathMatch: 'full' },
  { path: 'filter', component: SearchFilterComponent },
  { path: 'search', component: AutoSearchComponent },
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
