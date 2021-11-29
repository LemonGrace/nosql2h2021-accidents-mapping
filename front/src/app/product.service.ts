import {Injectable} from "@angular/core";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import { Observable, throwError } from 'rxjs';

@Injectable()
export class ProductService {
  constructor(protected http: HttpClient) {

  }

  public async GetBrands(): Promise<IItemsResponse[]> {
    let res_: IItemsResponse[] = [];

    this.http.get('http://127.0.0.1:8000/car/brands').subscribe(
      (value: any) => {
        for (let r of value["data"]["0"]) {
          r.logo = "http://127.0.0.1:8000/" + r.logo
          res_.push(r)
        }
      }
    );
    return res_;
  }
  public async GetModels(brand: string): Promise<IItemsModelsResponse[]> {
    let res_: IItemsModelsResponse[] = [];
    const url = 'http://127.0.0.1:8000/car' + brand;
    this.http.get(url).subscribe(
      (value: any) => {
        console.log(value)
        if (value){
          for (let r of value["data"]["0"]) {
            res_.push(r)
          }
        }
        else {
          res_.push({modelName: "", firstYearProduction: "", engineType: "", style: "",
            generations_count: ""})
        }
      }
    );
    console.log(res_)
    return res_;
  }

  public async GetGenerations(brand: string, model: string): Promise<IItemsGenerationResponse[]> {

    let res_: IItemsGenerationResponse[] = [];
    let url2 = 'http://127.0.0.1:8000/car/' + brand + '/' + model;
    this.http.get(url2).subscribe(
      (value: any) => {
        if (value){
          for (let r of value["data"]["0"]) {
            r.image = "http://127.0.0.1:8000/" + r.image
            console.log(r)
            res_.push(r)
          }
        }
      }
    );
    console.log(res_)
    return res_;
  }
}

export interface IItemsResponse {
  brand: string,
  logo: string
}

export interface IItemsModelsResponse {
  modelName: string,
  firstYearProduction:string,
  engineType: string,
  style: string,
  generations_count: string
}

export interface IItemsGenerationResponse {
  fullName: string,
  firstYearProduction: string,
  lastYearProduction: string,
  topSpeed: string,
  acceleration: string,
  lenght: string,
  width: string,
  height: string,
  wheelBase: string,
  wheelTrack: string,
  cargoVolume: string,
  aerodynamics: string,
  driveType: string,
  gearBox: string,
  fuel: string,
  image: string
}
