import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { SearchBarComponent } from './search-bar/search-bar.component';
import { SearchFilterComponent } from './search-filter/search-filter.component';


const routes: Routes = [
  { path: '', redirectTo: '/search', pathMatch: 'full' },
  { path: 'filter', component: SearchFilterComponent },
  { path: 'search', component: SearchBarComponent },
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
