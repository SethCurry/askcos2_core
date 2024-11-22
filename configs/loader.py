import json
import typing as t

from dataclasses import dataclass

class Validatable[T]:
  def __init__(self, validator: t.Callable[[T], None]):
    self.validator = validator

  def __call__(self, value: T) -> T:
    self.validator(value)

    return value
  
def __repo_validator(repo: str) -> None:
  if not repo.startswith("https://"):
    raise ValueError(f"Invalid repo, should start with 'https://': {repo}")

RepoField = Validatable(__repo_validator)

@dataclass
class ModuleStartConfig:
  atom_map_indigo: bool
  atom_map_rxnmapper: bool
  atom_map_wln: bool
  cluster: bool
  context_recommender: bool
  count_analogs: bool
  descriptors: bool
  evaluate_reactions: bool
  fast_filter: bool
  forward_augmented_transformer: bool
  forward_graph2smiles: bool
  forward_wldn5: bool
  general_selectivity: bool
  impurity_predictor: bool
  pathway_ranker: bool
  pmi_calculator: bool
  qm_descriptors: bool
  reaction_classification: bool
  retro_augmented_transformer: bool
  retro_graph2smiles: bool
  retro_retrosim: bool
  retro_template_relevance: bool
  scscore: bool
  site_selectivity: bool
  solubility: bool
  tree_search_expand_one: bool
  tree_search_mcts: bool
  tree_search_retro_star: bool

@dataclass
class GlobalConfig:
  require_frontend: bool
  container_runtime: str
  image_policy: str
  enable_gpu: bool

@dataclass
class DeploymentConfig:
  deployment_config: str
  use_gpu: bool
  ports_to_expose: t.List[int]
  default_prediction_url: str
  custom_prediction_url: str
  timeout: int
  available_model_names: t.List[str]

@dataclass
class ModuleConfig:
  repo: str
  description: str
  deployment: DeploymentConfig

  def validate(self) -> None:
    __repo_validator(self.repo)

@dataclass
class UtilConfig:
  engine: str
  database: str
  collection: str

class HistorianConfig(UtilConfig):
  files: t.List[str]

class PricerConfig(UtilConfig):
  file: str
  precompute_mols: bool

@dataclass
class ReactionsConfig:
  force_recompute_mols: bool

@dataclass
class SelectivityRefsConfig:
  file: str

@dataclass
class Config:
  modules_to_start: ModuleStartConfig
  global_config: GlobalConfig
  atom_map_indigo: ModuleConfig
  atom_map_rxnmapper: ModuleConfig
  atom_map_wln: ModuleConfig
  cluster: ModuleConfig
  context_recommender: ModuleConfig
  count_analogs: ModuleConfig
  descriptors: ModuleConfig
  evaluate_reactions: ModuleConfig
  fast_filter: ModuleConfig
  forward_augmented_transformer: ModuleConfig
  forward_graph2smiles: ModuleConfig
  forward_wldn5: ModuleConfig
  general_selectivity: ModuleConfig
  impurity_predictor: ModuleConfig
  pathway_ranker: ModuleConfig
  pmi_calculator: ModuleConfig
  qm_descriptors: ModuleConfig
  reaction_classification: ModuleConfig
  retro_augmented_transformer: ModuleConfig
  retro_graph2smiles: ModuleConfig
  retro_retrosim: ModuleConfig
  retro_template_relevance: ModuleConfig
  scscore: ModuleConfig
  site_selectivity: ModuleConfig
  solubility: ModuleConfig
  tree_search_expand_one: ModuleConfig
  tree_search_mcts: ModuleConfig
  tree_search_retro_star: ModuleConfig
  banned_chemicals: UtilConfig
  banned_reactions: UtilConfig
  historian: HistorianConfig
  pricer: PricerConfig
  reactions: ReactionsConfig
  selectivity_refs: SelectivityRefsConfig
  tree_search_results_controller: UtilConfig
  user_controller: UtilConfig
  frontend_config_controller: UtilConfig

def load_config(contents: str) -> Config:
  loaded = json.loads(contents)

  return Config(**loaded)
