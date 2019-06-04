import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { Router } from '@angular/router';
import { SearchService } from '../search.service'

import { Area} from '../models/area';

@Component({
  selector: 'app-auto-search',
  templateUrl: './auto-search.component.html',
  styleUrls: ['./auto-search.component.css']
})


export class AutoSearchComponent implements OnInit {
  constructor(public router: Router, private search: SearchService){}
  
  myControl = new FormControl();
  options: string[] = [];
  filteredOptions: Observable<string[]>;
  areas: Area[] = [];

  ngOnInit() {
    
    this.search.getAllAreas().subscribe((areas: Area[]) => {
      this.areas = areas;
      var option = this.areas.map(obj => obj.area);
      this.options = option;
     console.log(this.options);
    });
    
    this.filteredOptions = this.myControl.valueChanges
      .pipe(
        startWith(''),
        map(value => this._filter(value))
      );
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

  redirect() {
    this.router.navigate(['filter']);
  }
}