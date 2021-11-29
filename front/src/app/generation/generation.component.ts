import { Component, OnInit } from '@angular/core';
import {IItemsGenerationResponse, IItemsModelsResponse, ProductService} from "../product.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-generation',
  templateUrl: './generation.component.html',
  styleUrls: ['./generation.component.css']
})
export class GenerationComponent implements OnInit {
  public Generatins: IItemsGenerationResponse[] | undefined;
  public Init: boolean = false;
  public ModelName: string | undefined;
  public Brand: string;
  private readonly _modelName: string;

  constructor(
    protected productService: ProductService,
    protected router: Router,
    protected nav: Router
  ) {
    console.log(this.router.url)
    this._modelName = this.router.url.split("/")[2]
    this.Brand = this.router.url.split("/")[1]
  }

  public async ngOnInit(): Promise<void> {
    console.log(this._modelName);
    console.log(this.Brand)
    if (!this._modelName) {
      return;
    }
    this.Generatins = await this.productService.GetGenerations(this.Brand, this._modelName);
    this.Init = true;
  }

  public getModelName(): string {
    if (this._modelName.indexOf("%20") != -1){
      let model = this._modelName.split('%20')
      console.log(model)
      let modelName = model[0]
      for (let i = 1; i < model.length; i++) {
        modelName += ' ' + model[i]
      }
      return modelName;
    }
    return this._modelName;
  }

}
