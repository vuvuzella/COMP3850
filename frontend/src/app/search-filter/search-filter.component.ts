import { Component, OnInit } from '@angular/core';

import { Observable, of } from 'rxjs';
import { FormControl } from '@angular/forms';
import { map, startWith } from 'rxjs/operators';

import { Router, ActivatedRoute } from '@angular/router';
import { SearchService } from '../search.service'

import { Area } from '../models/area';
import { Cluster } from '../models/cluster';
import { Path } from '../models/path';
import { Points } from '../models/points';

declare function setPath(number): any;

@Component({
  selector: 'app-search-filter',
  templateUrl: './search-filter.component.html',
  styleUrls: ['./search-filter.component.css']
})
export class SearchFilterComponent implements OnInit {

  constructor(private searchService: SearchService, private router: Router, private route: ActivatedRoute) { }

  areaSearch = new FormControl();
  clusterSearch = new FormControl();
  pathSearch = new FormControl();

  options: string[] = [];
  filteredAreas: Observable<string[]>;
  areas: Area[] = [];
  clusters: Cluster[] = [];
  paths: Path[] = [];
  points: Points[] = [];
  pathOptions: Observable<string[]>;
  clusterOptions: Observable<string[]>;

  param: string;

  ngOnInit(): void {

    this.searchService.getAllAreas().subscribe((areas: Area[]) => {
      this.areas = areas;
      var option = this.areas.map(obj => obj.area);
      this.options = option;
    });

    this.param = this.route.snapshot.paramMap.get('area');

    this.areaSearch.setValue(this.param);

    this.searchService.getAreaClusters(this.param).subscribe((clusters: Cluster[]) => {
      this.clusters = clusters;
      var option = this.clusters.map(obj => obj.cluster)
      this.clusterOptions = of(option);
    });

    this.filteredAreas = this.areaSearch.valueChanges
      .pipe(
        startWith(''),
        map(value => this._filter(value))
      );
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().includes(filterValue));
  }

  findPaths() {
    this.searchService.getClusterPaths(this.clusterSearch.value).subscribe((paths: Path[]) => {
      var option = paths.map(obj => obj.path)
      this.pathOptions = of(option);
    })
  }

  findPoints() {
    if (this.pathSearch.value != '') {
      this.searchService.getPathPoints(this.pathSearch.value).subscribe((points: Points[]) => {
        var p = points.map(obj => obj.points);
        var pointValues = [].concat.apply([], p);
        console.log(pointValues);
        var x = [{lat: 0, lng: 0}];
        for (var i = 0;  i < pointValues.length; i++) {
          if (!(i % 2)) {
            x [i] = {lat: pointValues[i], lng: pointValues[i+1]}
          }
        }
        console.log(x);
        var pathCoordinates = [];
        for (var i = 0;  i < (x.length); i++) {
          if (x[i] != null) {
            pathCoordinates.push(x[i]);
          }  
        }
        console.log(pathCoordinates);
        setPath(pathCoordinates);
      })
    }
  }

  redirect() {
    this.router.navigate(['filter', {area: this.areaSearch.value}]);
  }
}